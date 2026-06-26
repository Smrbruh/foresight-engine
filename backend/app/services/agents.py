from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
from typing import List, Optional
from app.schemas.agents import AgentCreate, AgentUpdate, AgentResponse, AgentStatus
from app.models.agent import Agent

class AgentsService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def list_agents(self, limit: int, offset: int) -> List[AgentResponse]:
        stmt = select(Agent).limit(limit).offset(offset)
        result = await self.db.execute(stmt)
        agents = result.scalars().all()
        
        return [
            AgentResponse(
                id=a.id,
                name=a.name,
                type=a.type,
                description=a.description,
                status=a.status,
                config=a.config,
                last_seen=a.last_seen,
                created_at=a.created_at
            )
            for a in agents
        ]
    
    async def create_agent(self, data: AgentCreate) -> AgentResponse:
        agent = Agent(
            name=data.name,
            type=data.type,
            description=data.description,
            status=data.status or AgentStatus.ACTIVE,
            config=data.config or {}
        )
        self.db.add(agent)
        await self.db.commit()
        await self.db.refresh(agent)
        
        return AgentResponse(
            id=agent.id,
            name=agent.name,
            type=agent.type,
            description=agent.description,
            status=agent.status,
            config=agent.config,
            last_seen=agent.last_seen,
            created_at=agent.created_at
        )
    
    async def get_agent(self, agent_id: int) -> Optional[AgentResponse]:
        stmt = select(Agent).where(Agent.id == agent_id)
        result = await self.db.execute(stmt)
        agent = result.scalar_one_or_none()
        
        if not agent:
            return None
        
        return AgentResponse(
            id=agent.id,
            name=agent.name,
            type=agent.type,
            description=agent.description,
            status=agent.status,
            config=agent.config,
            last_seen=agent.last_seen,
            created_at=agent.created_at
        )
    
    async def update_agent(self, agent_id: int, data: AgentUpdate) -> AgentResponse:
        agent = await self.get_agent(agent_id)
        if not agent:
            raise ValueError("Agent not found")
        
        if data.name is not None:
            agent.name = data.name
        if data.description is not None:
            agent.description = data.description
        if data.status is not None:
            agent.status = data.status
        if data.config is not None:
            agent.config = data.config
        
        await self.db.commit()
        await self.db.refresh(agent)
        
        return agent
    
    async def delete_agent(self, agent_id: int):
        agent = await self.get_agent(agent_id)
        if agent:
            await self.db.delete(agent)
            await self.db.commit()