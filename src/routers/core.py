"""Core orchestration router for end-to-end workflows"""

from fastapi import APIRouter, Depends, HTTPException
from src.auth import verify_api_key, verify_jwt_token
from src.data.database import Database
from src.lm_adapter import LMAdapter
from src.agents.evaluator_agent import EvaluatorAgent
from src.agents.rl_agent import RLLoop
from src.schemas.spec_schema import Spec, ObjectSpec, SceneSpec
from pydantic import BaseModel
from typing import Dict, Any, Optional
import uuid
import time

router = APIRouter()

class CoreRunRequest(BaseModel):
    prompt: str
    iterations: int = 3
    store_results: bool = True
    compliance_check: bool = False
    project_id: Optional[str] = None

class CoreRunResponse(BaseModel):
    success: bool
    pipeline_id: str
    generated_spec: Dict[str, Any]
    evaluation_result: Dict[str, Any]
    iteration_results: Dict[str, Any]
    storage_info: Dict[str, Any]
    compliance_result: Optional[Dict[str, Any]] = None
    processing_time: float

def get_lm_adapter():
    return LMAdapter()

def get_evaluator():
    return EvaluatorAgent()

def get_rl_agent():
    return RLLoop()

def get_database():
    return Database()

@router.post("/core/run", response_model=CoreRunResponse)
async def run_core_pipeline(
    body: CoreRunRequest,
    api_key: str = Depends(verify_api_key),
    token: str = Depends(verify_jwt_token),
    lm: LMAdapter = Depends(get_lm_adapter),
    evaluator: EvaluatorAgent = Depends(get_evaluator),
    rl_agent: RLLoop = Depends(get_rl_agent),
    db: Database = Depends(get_database)
):
    """Core orchestration: generate → evaluate → iterate → store"""
    start_time = time.time()
    pipeline_id = str(uuid.uuid4())
    
    try:
        # Step 1: Generate specification
        print(f"[PIPELINE {pipeline_id}] Step 1: Generating spec...")
        lm_result = lm.run(body.prompt)
        
        # Build spec from LM result
        spec = build_spec_from_result(lm_result, pipeline_id)
        
        # Step 2: Evaluate specification
        print(f"[PIPELINE {pipeline_id}] Step 2: Evaluating spec...")
        evaluation = evaluator.run(spec, body.prompt)
        
        # Step 3: Iterate with RL (if requested)
        iteration_results = {}
        if body.iterations > 0:
            print(f"[PIPELINE {pipeline_id}] Step 3: Running {body.iterations} RL iterations...")
            rl_agent.max_iterations = body.iterations
            iteration_results = rl_agent.run(body.prompt, body.iterations)
        
        # Step 4: Store results
        storage_info = {}
        if body.store_results:
            print(f"[PIPELINE {pipeline_id}] Step 4: Storing results...")
            
            # Save spec
            spec_id = await db.save_spec_async(body.prompt, spec.dict(), "CorePipeline")
            
            # Save evaluation
            eval_id = await db.save_eval_async(spec_id, body.prompt, evaluation.dict(), evaluation.score)
            
            # Save iteration results if available
            iteration_id = None
            if iteration_results:
                iteration_id = await db.save_iteration_results(pipeline_id, iteration_results)
            
            storage_info = {
                "spec_id": spec_id,
                "eval_id": eval_id,
                "iteration_id": iteration_id,
                "pipeline_id": pipeline_id
            }
        
        # Step 5: Compliance check (optional)
        compliance_result = None
        if body.compliance_check:
            print(f"[PIPELINE {pipeline_id}] Step 5: Running compliance check...")
            compliance_result = await run_compliance_check(spec, body.project_id or pipeline_id, db)
        
        processing_time = time.time() - start_time
        
        print(f"[PIPELINE {pipeline_id}] Complete in {processing_time:.2f}s")
        
        return CoreRunResponse(
            success=True,
            pipeline_id=pipeline_id,
            generated_spec=spec.dict(),
            evaluation_result=evaluation.dict(),
            iteration_results=iteration_results,
            storage_info=storage_info,
            compliance_result=compliance_result,
            processing_time=processing_time
        )
        
    except Exception as e:
        processing_time = time.time() - start_time
        print(f"[PIPELINE {pipeline_id}] Failed after {processing_time:.2f}s: {e}")
        raise HTTPException(status_code=500, detail=f"Pipeline failed: {str(e)}")

def build_spec_from_result(lm_result: dict, pipeline_id: str) -> Spec:
    """Build Spec object from LM result"""
    
    # Extract objects
    objects = []
    if "objects" in lm_result:
        for obj_data in lm_result["objects"]:
            objects.append(ObjectSpec(**obj_data))
    else:
        # Default object
        objects.append(ObjectSpec(
            id="core_obj_001",
            type="main_structure",
            material=lm_result.get("materials", [{"type": "steel"}])[0].get("type", "steel"),
            editable=True,
            properties={"generated_by": "core_pipeline"}
        ))
    
    # Extract scene
    scene_data = lm_result.get("scene", {})
    scene = SceneSpec(**scene_data)
    
    return Spec(
        spec_id=f"core_{pipeline_id}",
        objects=objects,
        scene=scene,
        design_type=lm_result.get("design_type"),
        metadata={
            "pipeline_id": pipeline_id,
            "generated_by": "core_orchestration"
        }
    )

async def run_compliance_check(spec: Spec, project_id: str, db: Database) -> Dict[str, Any]:
    """Run compliance check on generated spec"""
    try:
        # Mock compliance check (replace with actual Soham integration)
        compliance_result = {
            "case_id": f"compliance_{spec.spec_id}",
            "project_id": project_id,
            "status": "passed",
            "violations": [],
            "recommendations": ["Consider adding fire safety features"],
            "geometry_url": f"/geometry/{spec.spec_id}.stl"
        }
        
        # Save compliance result
        await db.save_compliance_case(
            case_id=compliance_result["case_id"],
            project_id=project_id,
            case_data={"spec_id": spec.spec_id, "spec_data": spec.dict()},
            result=compliance_result
        )
        
        return compliance_result
        
    except Exception as e:
        print(f"Compliance check failed: {e}")
        return {"status": "error", "message": str(e)}