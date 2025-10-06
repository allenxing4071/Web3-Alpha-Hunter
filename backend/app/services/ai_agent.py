"""
AI智能助理核心服务
负责主动搜索、分析、学习、推荐项目和KOL
"""
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
import json
from datetime import datetime, timedelta

from app.core.config import settings


class AIAgent:
    """AI智能助理"""
    
    def __init__(self, db: Session):
        self.db = db
        self.config = self._load_work_config()
    
    def _load_work_config(self) -> Dict[str, Any]:
        """加载AI工作配置"""
        result = self.db.execute(text("""
            SELECT 
                primary_goal, target_roi, risk_tolerance, min_ai_score,
                required_cross_validation, min_platforms,
                search_lookback_hours, project_age_limit_days,
                max_projects_per_day, max_kols_per_day, rules
            FROM ai_work_config
            WHERE id = 1
        """))
        
        row = result.fetchone()
        if row:
            return {
                'primary_goal': row[0],
                'target_roi': row[1],
                'risk_tolerance': row[2],
                'min_ai_score': row[3],
                'required_cross_validation': row[4],
                'min_platforms': row[5],
                'search_lookback_hours': row[6],
                'project_age_limit_days': row[7],
                'max_projects_per_day': row[8],
                'max_kols_per_day': row[9],
                'rules': row[10] or {}
            }
        
        # 默认配置
        return {
            'primary_goal': '发现未发币的早期优质Web3项目',
            'target_roi': 50.0,
            'risk_tolerance': 'aggressive',
            'min_ai_score': 70.0,
            'required_cross_validation': True,
            'min_platforms': 2,
            'search_lookback_hours': 24,
            'project_age_limit_days': 180,
            'max_projects_per_day': 50,
            'max_kols_per_day': 20,
            'rules': {}
        }
    
    def analyze_project(self, raw_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        分析项目数据
        
        参数:
            raw_data: 原始采集数据 {
                'name': str,
                'description': str,
                'source': str,  # twitter, telegram, discord
                'source_url': str,
                'content': str,  # 原始内容
                ...
            }
        
        返回:
            分析结果或None (如果不符合标准)
        """
        
        # 1. 提取基础信息
        project_name = raw_data.get('name', '')
        description = raw_data.get('description', '')
        
        # 2. 初步评分（这里是模拟，实际应调用AI API）
        scores = self._calculate_scores(raw_data)
        
        # 3. 综合评分
        overall_score = self._calculate_overall_score(scores)
        
        # 4. 检查是否符合最低标准
        if overall_score < self.config['min_ai_score']:
            return None
        
        # 5. 生成推荐理由
        reasons = self._generate_recommendation_reasons(raw_data, scores)
        
        # 6. 确定等级
        grade = self._determine_grade(overall_score)
        
        # 7. 计算置信度
        confidence = self._calculate_confidence(raw_data, scores)
        
        return {
            'project_name': project_name,
            'symbol': raw_data.get('symbol'),
            'description': description,
            'discovered_from': raw_data.get('source'),
            'source_url': raw_data.get('source_url'),
            'source_content': raw_data.get('content', ''),
            'ai_score': overall_score,
            'ai_grade': grade,
            'ai_confidence': confidence,
            'ai_team_score': scores['team'],
            'ai_tech_score': scores['tech'],
            'ai_community_score': scores['community'],
            'ai_tokenomics_score': scores['tokenomics'],
            'ai_market_score': scores['market'],
            'ai_risk_score': scores['risk'],
            'ai_recommendation_reason': {
                'reasons': reasons,
                'scores': scores
            },
            'ai_extracted_info': {
                'website': raw_data.get('website'),
                'twitter': raw_data.get('twitter'),
                'telegram': raw_data.get('telegram'),
                'discord': raw_data.get('discord')
            }
        }
    
    def _calculate_scores(self, data: Dict[str, Any]) -> Dict[str, float]:
        """计算各维度评分（模拟，实际应调用AI API）"""
        
        # 这里是简化版评分逻辑
        # 实际应该调用DeepSeek/Claude/OpenAI进行深度分析
        
        rules = self.config.get('rules', {})
        weights = rules.get('scoring_weights', {
            'team': 0.20,
            'tech': 0.25,
            'community': 0.20,
            'tokenomics': 0.15,
            'market': 0.10,
            'risk': 0.10
        })
        
        # 团队评分
        team_score = 50.0
        if data.get('team_public'):
            team_score += 20
        if data.get('team_experienced'):
            team_score += 20
        if data.get('team_doxxed'):
            team_score += 10
        
        # 技术评分
        tech_score = 50.0
        if data.get('has_github'):
            tech_score += 15
        if data.get('has_whitepaper'):
            tech_score += 15
        if data.get('innovation_level', 0) > 7:
            tech_score += 20
        
        # 社区评分
        community_score = 50.0
        followers = data.get('followers', 0)
        if followers > 10000:
            community_score += 20
        elif followers > 5000:
            community_score += 10
        
        engagement = data.get('engagement_rate', 0)
        if engagement > 5:
            community_score += 20
        elif engagement > 2:
            community_score += 10
        
        # 代币经济评分
        tokenomics_score = 50.0
        if data.get('has_token_plan'):
            tokenomics_score += 20
        if data.get('fair_launch'):
            tokenomics_score += 30
        
        # 市场时机评分
        market_score = 60.0
        if data.get('trending'):
            market_score += 20
        if data.get('vc_backed'):
            market_score += 20
        
        # 风险评分（越低越好）
        risk_score = 80.0  # 基础低风险
        if data.get('red_flags', []):
            risk_score -= len(data['red_flags']) * 20
        
        return {
            'team': min(100, team_score),
            'tech': min(100, tech_score),
            'community': min(100, community_score),
            'tokenomics': min(100, tokenomics_score),
            'market': min(100, market_score),
            'risk': max(0, risk_score)
        }
    
    def _calculate_overall_score(self, scores: Dict[str, float]) -> float:
        """计算综合评分"""
        rules = self.config.get('rules', {})
        weights = rules.get('scoring_weights', {
            'team': 0.20,
            'tech': 0.25,
            'community': 0.20,
            'tokenomics': 0.15,
            'market': 0.10,
            'risk': 0.10
        })
        
        overall = sum(scores[key] * weights.get(key, 0) for key in scores.keys())
        return round(overall, 2)
    
    def _determine_grade(self, score: float) -> str:
        """根据评分确定等级"""
        if score >= 90:
            return 'S'
        elif score >= 80:
            return 'A'
        elif score >= 70:
            return 'B'
        else:
            return 'C'
    
    def _calculate_confidence(self, data: Dict[str, Any], scores: Dict[str, float]) -> float:
        """计算AI置信度"""
        confidence = 0.5  # 基础置信度
        
        # 数据完整性
        required_fields = ['name', 'description', 'website', 'twitter']
        completeness = sum(1 for f in required_fields if data.get(f)) / len(required_fields)
        confidence += completeness * 0.2
        
        # 评分一致性
        score_variance = max(scores.values()) - min(scores.values())
        if score_variance < 20:
            confidence += 0.2
        elif score_variance < 40:
            confidence += 0.1
        
        # 多平台验证
        if data.get('cross_platform_verified'):
            confidence += 0.1
        
        return min(1.0, confidence)
    
    def _generate_recommendation_reasons(
        self, 
        data: Dict[str, Any], 
        scores: Dict[str, float]
    ) -> List[str]:
        """生成推荐理由"""
        reasons = []
        
        # 根据高分维度生成理由
        if scores['team'] >= 80:
            reasons.append('团队背景优秀，成员经验丰富')
        
        if scores['tech'] >= 80:
            reasons.append('技术创新明显，有独特优势')
        
        if scores['community'] >= 80:
            reasons.append('社区活跃度高，用户参与度好')
        
        if scores['tokenomics'] >= 80:
            reasons.append('代币经济设计合理，分配公平')
        
        if scores['market'] >= 80:
            reasons.append('市场时机好，符合当前趋势')
        
        if scores['risk'] >= 80:
            reasons.append('风险较低，无明显红旗信号')
        
        # 特殊亮点
        if data.get('vc_backed'):
            reasons.append(f"获得知名VC投资: {data.get('vc_names', '未知')}")
        
        if data.get('followers', 0) > 50000:
            reasons.append(f"社交媒体粉丝数: {data['followers']:,}")
        
        if data.get('github_stars', 0) > 1000:
            reasons.append(f"GitHub星标: {data['github_stars']:,}")
        
        # 如果理由不足，添加通用理由
        if not reasons:
            reasons.append('综合评分达到推荐标准')
        
        return reasons
    
    def save_to_pending(self, analysis: Dict[str, Any]) -> int:
        """保存到待审核表"""
        result = self.db.execute(text("""
            INSERT INTO projects_pending (
                project_name, symbol, description,
                discovered_from, source_url, source_content,
                ai_score, ai_grade, ai_confidence,
                ai_team_score, ai_tech_score, ai_community_score,
                ai_tokenomics_score, ai_market_score, ai_risk_score,
                ai_recommendation_reason, ai_extracted_info,
                review_status, created_at, updated_at
            ) VALUES (
                :project_name, :symbol, :description,
                :discovered_from, :source_url, :source_content,
                :ai_score, :ai_grade, :ai_confidence,
                :ai_team_score, :ai_tech_score, :ai_community_score,
                :ai_tokenomics_score, :ai_market_score, :ai_risk_score,
                :ai_recommendation_reason, :ai_extracted_info,
                'pending', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
            )
            RETURNING id
        """), {
            'project_name': analysis['project_name'],
            'symbol': analysis.get('symbol'),
            'description': analysis.get('description'),
            'discovered_from': analysis['discovered_from'],
            'source_url': analysis.get('source_url'),
            'source_content': analysis.get('source_content'),
            'ai_score': analysis['ai_score'],
            'ai_grade': analysis['ai_grade'],
            'ai_confidence': analysis['ai_confidence'],
            'ai_team_score': analysis.get('ai_team_score', 0),
            'ai_tech_score': analysis.get('ai_tech_score', 0),
            'ai_community_score': analysis.get('ai_community_score', 0),
            'ai_tokenomics_score': analysis.get('ai_tokenomics_score', 0),
            'ai_market_score': analysis.get('ai_market_score', 0),
            'ai_risk_score': analysis.get('ai_risk_score', 0),
            'ai_recommendation_reason': json.dumps(analysis.get('ai_recommendation_reason', {})),
            'ai_extracted_info': json.dumps(analysis.get('ai_extracted_info', {}))
        })
        
        self.db.commit()
        return result.fetchone()[0]
    
    def check_daily_quota(self) -> Dict[str, Any]:
        """检查今日推荐配额"""
        today = datetime.now().date()
        
        result = self.db.execute(text("""
            SELECT COUNT(*) FROM projects_pending
            WHERE DATE(created_at) = :today
        """), {"today": today})
        
        today_count = result.fetchone()[0]
        
        return {
            'today_recommended': today_count,
            'max_allowed': self.config['max_projects_per_day'],
            'can_recommend': today_count < self.config['max_projects_per_day']
        }
    
    def learn_from_feedback(self, feedback: Dict[str, Any]):
        """从用户反馈中学习"""
        
        # 记录反馈
        self.db.execute(text("""
            INSERT INTO ai_learning_feedback (
                feedback_type, related_project_id, user_decision, user_reason, created_at
            ) VALUES (
                :feedback_type, :project_id, :decision, :reason, CURRENT_TIMESTAMP
            )
        """), {
            'feedback_type': 'project_review',
            'project_id': feedback['project_id'],
            'decision': feedback['decision'],  # approved, rejected
            'reason': feedback.get('reason')
        })
        
        self.db.commit()
        
        # TODO: 分析反馈模式，调整评分权重
        # 例如：如果用户频繁拒绝某类项目，降低该类特征的权重
    
    def get_learning_stats(self) -> Dict[str, Any]:
        """获取学习统计"""
        
        # 统计最近30天的审核情况
        result = self.db.execute(text("""
            SELECT 
                user_decision,
                COUNT(*) as count
            FROM ai_learning_feedback
            WHERE feedback_type = 'project_review'
                AND created_at >= CURRENT_DATE - INTERVAL '30 days'
            GROUP BY user_decision
        """))
        
        stats = {}
        for row in result:
            stats[row[0]] = row[1]
        
        total = sum(stats.values())
        approval_rate = stats.get('approved', 0) / total if total > 0 else 0
        
        return {
            'total_reviews': total,
            'approved': stats.get('approved', 0),
            'rejected': stats.get('rejected', 0),
            'approval_rate': approval_rate,
            'suggestion': self._get_adjustment_suggestion(approval_rate)
        }
    
    def _get_adjustment_suggestion(self, approval_rate: float) -> str:
        """根据批准率给出调整建议"""
        if approval_rate < 0.3:
            return '批准率较低，建议提高推荐标准(增加min_ai_score)'
        elif approval_rate > 0.8:
            return '批准率较高，可以适当降低标准以发现更多机会'
        else:
            return '批准率正常，保持当前策略'


def create_ai_agent(db: Session) -> AIAgent:
    """工厂函数"""
    return AIAgent(db)

