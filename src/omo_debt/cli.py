"""
omo-debt CLI 入口
Command-line interface for Pattern 09 v2.0 debt scoring tool.
"""
from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from omo_debt.core.stage import identify_project_stage, get_stage_weights, get_normalization_factor
from omo_debt.core.scoring import calculate_score_v2, compare_debt_scores

console = Console()


@click.group()
@click.version_option(version="0.1.0", prog_name="omo-debt")
def cli():
    """
    omo-debt: Pattern 09 v2.0 债务评分工具
    
    基于项目生命周期阶段的技术债务评分与优先级管理工具。
    """
    pass


@cli.command()
@click.argument("project_path", type=click.Path(exists=True))
@click.option("--months", default=6, help="分析月数（默认 6）")
@click.option("--verbose", is_flag=True, help="显示详细信息")
def identify_stage(project_path: str, months: int, verbose: bool):
    """
    识别项目生命周期阶段
    
    分析 Git 提交历史，自动判断项目处于：
    - 快速演进期 (rapid_evolution): >30 commits/month
    - 稳定增长期 (stable_growth): 10-30 commits/month  
    - 维护期 (maintenance): <10 commits/month
    
    示例：
        omo-debt identify-stage /path/to/project
        omo-debt identify-stage . --months 12 --verbose
    """
    try:
        path = Path(project_path).resolve()
        console.print(f"\n[bold cyan]分析项目：[/bold cyan]{path}")
        
        # 调用核心算法
        result = identify_project_stage(str(path), months=months)
        
        # 创建结果表格
        table = Table(title="项目阶段识别结果", show_header=True, header_style="bold magenta")
        table.add_column("指标", style="cyan", width=20)
        table.add_column("值", style="green")
        
        table.add_row("分析周期", f"{months} 个月")
        table.add_row("总提交数", str(result.total_commits))
        table.add_row("月均提交", f"{result.monthly_avg:.1f}")
        table.add_row("识别阶段", result.stage)
        table.add_row("置信度", result.confidence)
        
        console.print(table)
        
        weights = get_stage_weights(result.stage)
        norm_factor = get_normalization_factor(result.stage)
        panel_content = f"""
[bold]推荐配置：[/bold]
• 权重比例：影响 {weights[0]:.2f} / 频繁度 {weights[1]:.2f} / 成本 {weights[2]:.2f}
• 归一化系数：{norm_factor:.1f}
• 使用建议：{result._get_recommendation()}
        """
        console.print(Panel(panel_content.strip(), title="[bold green]评分配置[/bold green]"))
        
        if verbose:
            console.print(f"\n[dim]项目路径：{path}[/dim]")
        
    except Exception as e:
        console.print(f"[bold red]错误：[/bold red]{e}", style="red")
        sys.exit(1)


@cli.command()
@click.option("--impact", type=float, required=True, help="影响分数 (1-10)")
@click.option("--frequency", type=float, required=True, help="频繁度分数 (1-10)")
@click.option("--cost", type=float, required=True, help="成本分数 (1-10)")
@click.option("--stage", type=click.Choice(["rapid_evolution", "stable_growth", "maintenance"]), 
              help="项目阶段（可选，不指定则自动检测）")
@click.option("--project-path", type=click.Path(exists=True), 
              help="项目路径（用于自动检测阶段）")
def score(impact: float, frequency: float, cost: float, 
          stage: Optional[str], project_path: Optional[str]):
    """
    计算技术债务加权分数
    
    使用 Pattern 09 v2.0 算法，根据项目阶段动态调整权重。
    
    示例：
        omo-debt score --impact 9 --frequency 8 --cost 7
        omo-debt score --impact 9 --frequency 8 --cost 7 --stage rapid_evolution
        omo-debt score --impact 9 --frequency 8 --cost 7 --project-path .
    """
    try:
        # 自动检测阶段（如果提供了项目路径）
        if project_path and not stage:
            console.print(f"[dim]自动检测项目阶段...[/dim]")
            stage_info = identify_project_stage(project_path)
            stage = stage_info.stage
            console.print(f"[dim]检测到阶段：{stage}[/dim]\n")
        
        # 计算分数
        result = calculate_score_v2(
            impact=impact,
            frequency=frequency, 
            cost=cost,
            stage=stage
        )
        
        # 显示结果
        table = Table(title="债务评分结果", show_header=True, header_style="bold magenta")
        table.add_column("指标", style="cyan", width=20)
        table.add_column("值", style="green")
        
        table.add_row("影响分数", f"{impact:.1f}")
        table.add_row("频繁度分数", f"{frequency:.1f}")
        table.add_row("成本分数", f"{cost:.1f}")
        table.add_row("项目阶段", result.stage or "N/A")
        table.add_row("基础分数", f"{result.base_score:.2f}")
        table.add_row("归一化系数", f"{result.normalization_factor:.1f}")
        table.add_row("最终分数", f"[bold]{result.normalized_score:.2f}[/bold]")
        
        # 优先级颜色
        priority = result.priority
        priority_color = {"P0": "red", "P1": "yellow", "P2": "green"}.get(priority, "white")
        table.add_row("优先级", f"[bold {priority_color}]{priority}[/bold {priority_color}]")
        
        console.print(table)
        
        # 显示建议 (DebtScore 没有 recommendation 字段，根据 priority 生成建议)
        if result.priority == "P0":
            recommendation = "🔴 极高优先级债务，建议立即安排资源处理"
        elif result.priority == "P1":
            recommendation = "🟡 高优先级债务，建议本迭代内处理"
        else:
            recommendation = "🟢 中等优先级债务，可适当延后处理"
        
        console.print(Panel(recommendation, title="[bold green]建议[/bold green]"))
        
    except Exception as e:
        console.print(f"[bold red]错误：[/bold red]{e}", style="red")
        sys.exit(1)


@cli.command()
@click.argument("debt_files", nargs=-1, type=click.Path(exists=True), required=True)
@click.option("--format", type=click.Choice(["table", "json", "yaml"]), default="table", 
              help="输出格式（默认 table）")
def compare(debt_files: tuple[str, ...], format: str):
    """
    对比多个债务项优先级
    
    读取多个债务 YAML 文件，按优先级排序输出。
    
    债务 YAML 格式：
        id: GBR-D01
        title: 未实现跨表关联查询
        impact: 9
        frequency: 8
        cost: 7
        stage: rapid_evolution  # 可选，不指定则使用 project_path 自动检测
        project: gbrain
    
    示例：
        omo-debt compare debt1.yaml debt2.yaml debt3.yaml
        omo-debt compare debts/*.yaml --format json
    """
    try:
        import yaml
        from pathlib import Path
        
        # 读取所有债务文件
        debts = []
        for file_path in debt_files:
            with open(file_path) as f:
                debt_data = yaml.safe_load(f)
                
                # 验证必需字段
                if not all(k in debt_data for k in ["impact", "frequency", "cost"]):
                    console.print(f"[yellow]⚠️  跳过 {file_path}：缺少必需字段（impact/frequency/cost）[/yellow]")
                    continue
                
                # 计算评分
                result = calculate_score_v2(
                    impact=debt_data["impact"],
                    frequency=debt_data["frequency"],
                    cost=debt_data["cost"],
                    stage=debt_data.get("stage")
                )
                
                debts.append({
                    "id": debt_data.get("id", Path(file_path).stem),
                    "title": debt_data.get("title", "未命名债务"),
                    "project": debt_data.get("project", "unknown"),
                    "stage": result.stage or "N/A",
                    "impact": debt_data["impact"],
                    "frequency": debt_data["frequency"],
                    "cost": debt_data["cost"],
                    "score": result.normalized_score,
                    "priority": result.priority,
                    "file": file_path
                })
        
        # 按优先级和分数排序
        debts.sort(key=lambda d: (
            {"P0": 0, "P1": 1, "P2": 2}[d["priority"]],
            -d["score"]
        ))
        
        # 输出结果
        if format == "table":
            table = Table(title=f"债务对比结果（共 {len(debts)} 项）", 
                         show_header=True, header_style="bold magenta")
            table.add_column("#", style="dim", width=4)
            table.add_column("ID", style="cyan", width=12)
            table.add_column("项目", style="blue", width=12)
            table.add_column("标题", style="white", width=30)
            table.add_column("阶段", style="yellow", width=16)
            table.add_column("分数", style="green", width=8)
            table.add_column("优先级", width=8)
            
            for i, debt in enumerate(debts, 1):
                priority_color = {"P0": "red", "P1": "yellow", "P2": "green"}[debt["priority"]]
                table.add_row(
                    str(i),
                    debt["id"],
                    debt["project"],
                    debt["title"][:28] + "..." if len(debt["title"]) > 28 else debt["title"],
                    debt["stage"],
                    f"{debt['score']:.2f}",
                    f"[{priority_color}]{debt['priority']}[/{priority_color}]"
                )
            
            console.print(table)
            
            # 统计信息
            p0_count = sum(1 for d in debts if d["priority"] == "P0")
            p1_count = sum(1 for d in debts if d["priority"] == "P1")
            p2_count = sum(1 for d in debts if d["priority"] == "P2")
            
            stats = f"""
[bold]优先级分布：[/bold]
• P0（极高优先级）：{p0_count} 项
• P1（高优先级）：{p1_count} 项
• P2（中等优先级）：{p2_count} 项
            """
            console.print(Panel(stats.strip(), title="[bold green]统计信息[/bold green]"))
            
        elif format == "json":
            import json
            console.print(json.dumps(debts, indent=2, ensure_ascii=False))
            
        elif format == "yaml":
            import yaml
            console.print(yaml.dump(debts, allow_unicode=True, default_flow_style=False))
        
    except Exception as e:
        console.print(f"[bold red]错误：[/bold red]{e}", style="red")
        sys.exit(1)


@cli.command()
@click.argument("project_path", type=click.Path(exists=True))
@click.option("--debt-file", type=click.Path(exists=True), 
              help="债务清单文件（YAML，包含 debts 列表）")
@click.option("--output", type=click.Path(), help="输出报告文件路径")
def analyze(project_path: str, debt_file: str | None, output: str | None):
    """
    分析项目债务健康度
    
    扫描项目，生成完整的债务健康报告。
    
    示例：
        omo-debt analyze /path/to/project
        omo-debt analyze . --debt-file debts.yaml
        omo-debt analyze . --debt-file debts.yaml --output report.md
    """
    try:
        from pathlib import Path
        
        path = Path(project_path).resolve()
        console.print(f"\n[bold cyan]分析项目：[/bold cyan]{path}")
        
        # 1. 识别项目阶段
        stage_info = identify_project_stage(str(path))
        console.print(f"[dim]项目阶段：{stage_info.stage}（月均 {stage_info.monthly_avg:.1f} 次提交）[/dim]")
        
        # 2. 读取债务清单
        debts = []
        if debt_file:
            import yaml
            with open(debt_file) as f:
                data = yaml.safe_load(f)
                debt_list = data.get("debts", []) if isinstance(data, dict) else data
                
                for debt_data in debt_list:
                    result = calculate_score_v2(
                        impact=debt_data["impact"],
                        frequency=debt_data["frequency"],
                        cost=debt_data["cost"],
                        stage=debt_data.get("stage") or stage_info.stage
                    )
                    
                    debts.append({
                        "id": debt_data.get("id", "未知"),
                        "title": debt_data.get("title", "未命名"),
                        "score": result.normalized_score,
                        "priority": result.priority
                    })
        
        # 3. 生成报告
        if debts:
            # 按优先级分组
            p0_debts = [d for d in debts if d["priority"] == "P0"]
            p1_debts = [d for d in debts if d["priority"] == "P1"]
            p2_debts = [d for d in debts if d["priority"] == "P2"]
            
            # 计算健康度分数（100 - 加权债务影响）
            health_score = max(0, 100 - (len(p0_debts) * 15 + len(p1_debts) * 8 + len(p2_debts) * 3))
            
            # 显示结果
            table = Table(title="项目债务健康报告", show_header=True, header_style="bold magenta")
            table.add_column("指标", style="cyan", width=20)
            table.add_column("值", style="green")
            
            table.add_row("项目路径", str(path))
            table.add_row("生命周期阶段", stage_info.stage)
            table.add_row("月均提交数", f"{stage_info.monthly_avg:.1f}")
            table.add_row("债务总数", str(len(debts)))
            table.add_row("P0（极高优先级）", str(len(p0_debts)))
            table.add_row("P1（高优先级）", str(len(p1_debts)))
            table.add_row("P2（中等优先级）", str(len(p2_debts)))
            
            # 健康度评级
            if health_score >= 80:
                health_grade = "🟢 优秀"
            elif health_score >= 60:
                health_grade = "🟡 良好"
            elif health_score >= 40:
                health_grade = "🟠 一般"
            else:
                health_grade = "🔴 需改进"
            
            table.add_row("健康度分数", f"{health_score}/100")
            table.add_row("健康度评级", health_grade)
            
            console.print(table)
            
            # 建议
            recommendations = []
            if len(p0_debts) > 0:
                recommendations.append(f"• {len(p0_debts)} 个 P0 债务需要立即处理")
            if len(p1_debts) > 3:
                recommendations.append(f"• {len(p1_debts)} 个 P1 债务较多，建议本迭代优先处理 3-5 个")
            if health_score < 60:
                recommendations.append("• 总体健康度较低，建议制定系统性还债计划")
            
            if recommendations:
                console.print(Panel("\n".join(recommendations), 
                                   title="[bold yellow]改进建议[/bold yellow]"))
            
            # 输出报告文件
            if output:
                report_content = f"""# 项目债务健康报告

**项目路径**：{path}  
**生命周期阶段**：{stage_info.stage}  
**月均提交数**：{stage_info.monthly_avg:.1f}  
**分析时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 债务概览

- **债务总数**：{len(debts)}
- **P0（极高优先级）**：{len(p0_debts)}
- **P1（高优先级）**：{len(p1_debts)}
- **P2（中等优先级）**：{len(p2_debts)}

## 健康度评估

- **健康度分数**：{health_score}/100
- **健康度评级**：{health_grade}

## 改进建议

{"".join(f"{r}\n" for r in recommendations)}

## 债务清单

### P0 债务（极高优先级）

{"".join(f"- [{d['id']}] {d['title']} (分数: {d['score']:.2f})\n" for d in p0_debts) if p0_debts else "无\n"}

### P1 债务（高优先级）

{"".join(f"- [{d['id']}] {d['title']} (分数: {d['score']:.2f})\n" for d in p1_debts) if p1_debts else "无\n"}

### P2 债务（中等优先级）

{"".join(f"- [{d['id']}] {d['title']} (分数: {d['score']:.2f})\n" for d in p2_debts) if p2_debts else "无\n"}
"""
                Path(output).write_text(report_content)
                console.print(f"\n[green]✓[/green] 报告已保存到：{output}")
        else:
            console.print("[yellow]未找到债务清单，请使用 --debt-file 指定债务文件[/yellow]")
            
    except Exception as e:
        console.print(f"[bold red]错误：[/bold red]{e}", style="red")
        sys.exit(1)


def main():
    """CLI 入口点"""
    cli()


if __name__ == "__main__":
    main()


# Import honesty assessment command
try:
    from omo_debt.cli_honesty import assess_honesty
    cli.add_command(assess_honesty)
except ImportError:
    pass  # Honesty module not available
