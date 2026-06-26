from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.agents import AgentCreate, AgentResponse, AgentUpdate
from app.services.agents import AgentsService

router = APIRouter()


@router.get("/", response_model=list[AgentResponse])
async def list_agents(limit: int = 50, offset: int = 0, db: AsyncSession = Depends(get_db)):
    service = AgentsService(db)
    return await service.list_agents(limit, offset)


@router.post("/", response_model=AgentResponse, status_code=201)
async def create_agent(data: AgentCreate, db: AsyncSession = Depends(get_db)):
    service = AgentsService(db)
    return await service.create_agent(data)


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: int, db: AsyncSession = Depends(get_db)):
    service = AgentsService(db)
    agent = await service.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@router.patch("/{agent_id}", response_model=AgentResponse)
async def update_agent(agent_id: int, data: AgentUpdate, db: AsyncSession = Depends(get_db)):
    service = AgentsService(db)
    return await service.update_agent(agent_id, data)


@router.delete("/{agent_id}", status_code=204)
async def delete_agent(agent_id: int, db: AsyncSession = Depends(get_db)):
    service = AgentsService(db)
    await service.delete_agent(agent_id)
