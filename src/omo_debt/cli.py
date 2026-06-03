"""
omo-debt CLI 入口
Command-line interface for Pattern 09 v2.0 debt scoring tool.
"""
from __future__ import annotations

import sys
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
@click.argument("debt_files", nargs=-1, type=click.Path(exists=True))
def compare(debt_files: tuple[str, ...]):
    """
    对比多个债务项优先级
    
    读取多个债务 YAML 文件，按优先级排序输出。
    
    示例：
        omo-debt compare debt1.yaml debt2.yaml debt3.yaml
    """
    console.print("[bold yellow]compare 命令开发中...[/bold yellow]")
    console.print(f"待对比文件：{list(debt_files)}")


@cli.command()
@click.argument("project_path", type=click.Path(exists=True))
def analyze(project_path: str):
    """
    分析项目债务健康度
    
    扫描项目，生成完整的债务健康报告。
    
    示例：
        omo-debt analyze /path/to/project
    """
    console.print("[bold yellow]analyze 命令开发中...[/bold yellow]")
    console.print(f"待分析项目：{project_path}")


def main():
    """CLI 入口点"""
    cli()


if __name__ == "__main__":
    main()
