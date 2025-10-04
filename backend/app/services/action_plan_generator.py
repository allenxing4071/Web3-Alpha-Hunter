"""投资行动指南生成器"""

from typing import Dict, List
from datetime import date, datetime, timedelta
from pydantic import BaseModel
from loguru import logger


class ActionStep(BaseModel):
    """行动步骤"""
    step_number: int
    action: str
    deadline: str
    cost_estimate: str
    status: str = "pending"
    priority: str
    notes: str = ""


class ActionPlan(BaseModel):
    """投资行动计划"""
    project_name: str
    project_tier: str
    composite_score: int
    
    total_budget: int
    budget_breakdown: Dict
    
    start_date: str
    target_duration: str
    urgency: str
    
    action_steps: List[ActionStep]
    
    monitoring_metrics: List[str]
    alert_conditions: List[str]
    
    risks: List[str]
    stop_loss_conditions: List[str]
    
    expected_roi: str
    airdrop_estimate: int


class ActionPlanGenerator:
    """行动计划生成器"""
    
    # 月预算
    MONTHLY_BUDGET = 20000  # CNY
    
    # 预算分配比例
    BUDGET_ALLOCATION = {
        "S": {"ratio": 0.40, "count": "2-3", "per_project": (2500, 4000)},
        "A": {"ratio": 0.40, "count": "3-4", "per_project": (2000, 2500)},
        "B": {"ratio": 0.10, "count": "2-3", "per_project": (500, 1000)},
    }
    
    def __init__(self):
        """初始化"""
        logger.info("✅ Action Plan Generator initialized")
    
    def calculate_project_budget(
        self,
        tier: str,
        score: int,
        launch_probability: float,
        airdrop_value: int,
        available_budget: int
    ) -> int:
        """计算单个项目的投入预算
        
        Args:
            tier: 项目分级 (S/A/B/C)
            score: 综合评分
            launch_probability: 发币概率
            airdrop_value: 预估空投价值
            available_budget: 可用预算
            
        Returns:
            项目预算（CNY）
        """
        if tier not in self.BUDGET_ALLOCATION:
            return 0
        
        # 基础预算
        min_budget, max_budget = self.BUDGET_ALLOCATION[tier]["per_project"]
        base = (min_budget + max_budget) / 2
        
        # 调整因子
        score_factor = 0.7 + (score - 70) * 0.006  # 评分调整
        prob_factor = 0.7 + launch_probability * 0.006  # 概率调整
        
        # 空投价值调整
        if airdrop_value > 5000:
            value_factor = 1.25
        elif airdrop_value > 3000:
            value_factor = 1.15
        elif airdrop_value > 1000:
            value_factor = 1.0
        else:
            value_factor = 0.85
        
        # 计算最终预算
        calculated = base * score_factor * prob_factor * value_factor
        
        # 限制范围
        max_allowed = available_budget * 0.3
        final = max(min_budget, min(calculated, max_allowed))
        
        return int(final)
    
    def generate_defi_steps(self, project: Dict, budget: int) -> List[ActionStep]:
        """生成DeFi项目步骤"""
        steps = []
        
        steps.append(ActionStep(
            step_number=1,
            action="创建新钱包或准备专用钱包",
            deadline="立即",
            cost_estimate="¥0",
            priority="high",
            notes="建议使用新钱包，避免关联"
        ))
        
        steps.append(ActionStep(
            step_number=2,
            action=f"准备资金并桥接到{project.get('blockchain', 'Ethereum')}",
            deadline="24小时内",
            cost_estimate=f"¥{int(budget * 0.6)} + 跨链费约¥{int(budget * 0.05)}",
            priority="high",
            notes=f"主网: {project.get('blockchain')}"
        ))
        
        steps.append(ActionStep(
            step_number=3,
            action="加入官方社区（Twitter + Telegram + Discord）",
            deadline="24小时内",
            cost_estimate="¥0",
            priority="medium",
            notes="关注官方公告"
        ))
        
        steps.append(ActionStep(
            step_number=4,
            action=f"存入资金到协议（分3-5次，每次约¥{int(budget * 0.15)}）",
            deadline="3天内完成首次",
            cost_estimate=f"¥{int(budget * 0.6)}",
            priority="high",
            notes="分批操作更像真实用户"
        ))
        
        steps.append(ActionStep(
            step_number=5,
            action="执行多样化交易（至少10笔不同类型）",
            deadline="持续进行",
            cost_estimate=f"Gas费约¥{int(budget * 0.15)}",
            priority="high",
            notes="包括：存款、取款、Swap、添加流动性等"
        ))
        
        steps.append(ActionStep(
            step_number=6,
            action="保持协议活跃度（每周2-3笔交易）",
            deadline="持续至快照",
            cost_estimate="Gas费计入Step 5",
            priority="medium",
            notes="活跃用户通常获得更多空投"
        ))
        
        return steps
    
    def generate_l2_steps(self, project: Dict, budget: int) -> List[ActionStep]:
        """生成L2项目步骤"""
        steps = []
        
        # 前3步同DeFi
        steps.extend(self.generate_defi_steps(project, budget)[:3])
        
        steps.append(ActionStep(
            step_number=4,
            action=f"使用官方桥接资产到{project['project_name']}",
            deadline="3天内",
            cost_estimate=f"¥{int(budget * 0.5)} + 桥接费约¥{int(budget * 0.05)}",
            priority="high",
            notes=f"官方桥: {project.get('official_bridge', '见项目文档')}"
        ))
        
        steps.append(ActionStep(
            step_number=5,
            action="在L2上使用至少5个不同的Dapp",
            deadline="2周内完成首轮",
            cost_estimate=f"Gas费约¥{int(budget * 0.1)}（L2 Gas费较低）",
            priority="high",
            notes="包括：DEX、借贷、NFT市场、游戏等"
        ))
        
        steps.append(ActionStep(
            step_number=6,
            action="执行多样化交易（每个Dapp至少3笔）",
            deadline="持续进行",
            cost_estimate="Gas费计入Step 5",
            priority="high",
            notes="交易类型越多样，空投概率越大"
        ))
        
        return steps
    
    def generate_nft_steps(self, project: Dict, budget: int) -> List[ActionStep]:
        """生成NFT项目步骤"""
        steps = []
        
        steps.append(ActionStep(
            step_number=1,
            action="加入项目Discord并完成身份验证",
            deadline="立即",
            cost_estimate="¥0",
            priority="high",
            notes="Discord是NFT项目的核心社区"
        ))
        
        steps.append(ActionStep(
            step_number=2,
            action="获取社区身份角色",
            deadline="1周内",
            cost_estimate="¥0（时间成本）",
            priority="high",
            notes="有些角色是白名单的前提"
        ))
        
        steps.append(ActionStep(
            step_number=3,
            action="积极参与社区活动（每周至少5条发言）",
            deadline="持续进行",
            cost_estimate="¥0（时间成本）",
            priority="high",
            notes="活跃度是白名单筛选的重要指标"
        ))
        
        steps.append(ActionStep(
            step_number=4,
            action="完成Crew3/Zealy/Galxe平台任务",
            deadline="任务截止前",
            cost_estimate="¥0-200",
            priority="high",
            notes="查看项目公告了解具体平台"
        ))
        
        steps.append(ActionStep(
            step_number=5,
            action="白名单开放时立即申请",
            deadline="白名单开放时",
            cost_estimate="¥0",
            priority="critical",
            notes="设置提醒，避免错过"
        ))
        
        steps.append(ActionStep(
            step_number=6,
            action=f"Mint NFT（预算¥{int(budget * 0.7)}，建议2-3个）",
            deadline="Mint开启后2小时内",
            cost_estimate=f"¥{int(budget * 0.7)} + Gas费约¥{int(budget * 0.1)}",
            priority="critical",
            notes="设置好Gas，确保交易成功"
        ))
        
        return steps
    
    def calculate_budget_breakdown(self, budget: int, category: str) -> Dict:
        """计算预算明细"""
        if category == "DeFi":
            return {
                "协议存款": {"金额": int(budget * 0.60), "说明": "存入协议赚取收益"},
                "交易Gas费": {"金额": int(budget * 0.15), "说明": "各类交易手续费"},
                "跨链桥接费": {"金额": int(budget * 0.05), "说明": "资金桥接费用"},
                "应急储备": {"金额": int(budget * 0.20), "说明": "应对突发情况"}
            }
        elif category in ["L2", "Layer2"]:
            return {
                "桥接资产": {"金额": int(budget * 0.50), "说明": "桥接到L2的主要资金"},
                "Dapp交互": {"金额": int(budget * 0.20), "说明": "在各Dapp上的操作资金"},
                "Gas费": {"金额": int(budget * 0.10), "说明": "L1+L2的Gas费"},
                "应急储备": {"金额": int(budget * 0.20), "说明": "灵活应对"}
            }
        elif category == "NFT":
            return {
                "NFT Mint": {"金额": int(budget * 0.70), "说明": "铸造NFT的主要费用"},
                "Gas费": {"金额": int(budget * 0.15), "说明": "Mint时的Gas费"},
                "任务费用": {"金额": int(budget * 0.05), "说明": "完成链上任务费用"},
                "应急储备": {"金额": int(budget * 0.10), "说明": "应对意外"}
            }
        else:
            return {
                "主要参与资金": {"金额": int(budget * 0.70), "说明": "参与项目的主要资金"},
                "Gas和手续费": {"金额": int(budget * 0.15), "说明": "各类手续费"},
                "应急储备": {"金额": int(budget * 0.15), "说明": "灵活应对"}
            }
    
    def generate_monitoring_metrics(self, project: Dict) -> List[str]:
        """生成监控指标"""
        metrics = [
            "官方Twitter发布快照公告",
            "官方Telegram/Discord发布重要更新",
            "代币经济学文档发布",
            "审计报告发布",
            "融资消息",
            "竞品项目发币动态"
        ]
        
        category = project.get("category", "")
        
        if category == "DeFi":
            metrics.extend([
                "协议TVL变化（> ±20%需关注）",
                "智能合约升级",
                "流动性挖矿参数变化"
            ])
        elif category in ["L2", "Layer2"]:
            metrics.extend([
                "L2每日活跃地址数",
                "L2 TVL变化",
                "新Dapp上线"
            ])
        elif category == "NFT":
            metrics.extend([
                "Mint日期公告",
                "白名单抽选结果",
                "地板价变化"
            ])
        
        return metrics
    
    def generate_alert_conditions(self) -> List[str]:
        """生成预警条件"""
        return [
            "🚨 快照时间公告（Critical）",
            "🚨 白名单开放（Critical）",
            "🚨 Mint开始（Critical）",
            "⚠️ 代币经济学发布（High）",
            "⚠️ 审计报告有严重漏洞（High）",
            "⚠️ 官方声明延期（Medium）",
            "⚠️ 社区负面情绪激增（Medium）"
        ]
    
    def identify_risks(self, project: Dict, score: Dict) -> List[str]:
        """识别风险"""
        risks = []
        
        if score.get("team_score", 0) < 50:
            risks.append(f"⚠️ 团队背景评分较低（{score['team_score']}/100）")
        
        if score.get("risk_score", 0) < 50:
            risks.append(f"🚨 风险评分较低（{score['risk_score']}/100）")
        
        if not project.get("has_audit"):
            risks.append("⚠️ 智能合约未经审计")
        
        if project.get("team_anonymous"):
            risks.append("⚠️ 团队匿名，存在跑路风险")
        
        competitors = project.get("competitor_count", 0)
        if competitors > 5:
            risks.append(f"⚠️ 同类竞品较多（{competitors}个）")
        
        return risks
    
    def generate_stop_loss_conditions(self, budget: int) -> List[str]:
        """生成止损条件"""
        return [
            f"💸 资金损失 > ¥{int(budget * 0.5)}（50%）- 立即退出",
            f"💸 资金损失 > ¥{int(budget * 0.3)}（30%）- 评估是否退出",
            "🚨 智能合约被攻击 - 立即提现所有资金",
            "🚨 项目方跑路迹象 - 立即退出",
            "🚨 官方宣布项目终止 - 立即退出",
            "⚠️ 连续3个月无进展 - 考虑退出",
            "⚠️ TVL/用户暴跌（> 70%）- 考虑退出"
        ]
    
    def calculate_expected_roi(
        self,
        score: int,
        launch_prob: float,
        airdrop_value: int,
        budget: int
    ) -> str:
        """计算预期ROI"""
        if score >= 85:
            base_roi = 30
        elif score >= 70:
            base_roi = 15
        elif score >= 60:
            base_roi = 8
        else:
            base_roi = 3
        
        prob_adjusted = base_roi * (launch_prob / 100)
        
        if airdrop_value > 0:
            value_based = (airdrop_value * 6.5) / budget
            final_roi = prob_adjusted * 0.6 + value_based * 0.4
        else:
            final_roi = prob_adjusted
        
        return f"{final_roi:.1f}倍"
    
    def generate_action_plan(
        self,
        project: Dict,
        score: Dict,
        launch_prob: Dict,
        airdrop_value: Dict
    ) -> ActionPlan:
        """生成完整的投资行动计划
        
        Args:
            project: 项目数据
            score: 评分数据
            launch_prob: 发币概率数据
            airdrop_value: 空投价值数据
            
        Returns:
            行动计划
        """
        logger.info(f"📋 Generating action plan for {project['project_name']}")
        
        # 1. 计算预算
        tier = score.get("grade", "B")
        budget = self.calculate_project_budget(
            tier=tier,
            score=score.get("composite_score", 60),
            launch_probability=launch_prob.get("launch_probability", 50),
            airdrop_value=airdrop_value.get("estimated_value_usd", 1000),
            available_budget=self.MONTHLY_BUDGET
        )
        
        # 2. 生成步骤
        category = project.get("category", "DeFi")
        
        if category == "DeFi":
            steps = self.generate_defi_steps(project, budget)
        elif category in ["L2", "Layer2"]:
            steps = self.generate_l2_steps(project, budget)
        elif category == "NFT":
            steps = self.generate_nft_steps(project, budget)
        else:
            steps = self.generate_defi_steps(project, budget)
        
        # 3. 预算明细
        budget_breakdown = self.calculate_budget_breakdown(budget, category)
        
        # 4. 监控和风险
        monitoring = self.generate_monitoring_metrics(project)
        alerts = self.generate_alert_conditions()
        risks = self.identify_risks(project, score)
        stop_loss = self.generate_stop_loss_conditions(budget)
        
        # 5. ROI预估
        expected_roi = self.calculate_expected_roi(
            score.get("composite_score", 60),
            launch_prob.get("launch_probability", 50),
            airdrop_value.get("estimated_value_usd", 1000),
            budget
        )
        
        # 6. 评估紧迫性
        prob = launch_prob.get("launch_probability", 0)
        if prob >= 80:
            urgency = "Critical"
        elif prob >= 60:
            urgency = "High"
        else:
            urgency = "Normal"
        
        plan = ActionPlan(
            project_name=project["project_name"],
            project_tier=tier,
            composite_score=score.get("composite_score", 0),
            total_budget=budget,
            budget_breakdown=budget_breakdown,
            start_date=str(date.today()),
            target_duration=launch_prob.get("estimated_timeline", "1-3个月"),
            urgency=urgency,
            action_steps=steps,
            monitoring_metrics=monitoring,
            alert_conditions=alerts,
            risks=risks,
            stop_loss_conditions=stop_loss,
            expected_roi=expected_roi,
            airdrop_estimate=airdrop_value.get("estimated_value_usd", 0)
        )
        
        logger.info(f"✅ Action plan generated: Budget ¥{budget}, {len(steps)} steps")
        
        return plan


# 全局服务实例
action_plan_generator = ActionPlanGenerator()

