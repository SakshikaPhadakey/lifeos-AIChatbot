import json
import re


class WorkflowAgent:

    def build_workflow(self, llm_output: str):

        try:
            # remove markdown code blocks if present
            cleaned = re.sub(r"```json|```", "", llm_output).strip()

            data = json.loads(cleaned)

            return {
                "goal": data.get("goal", "Business Setup"),
                "workflow": data.get("workflow", [])
            }

        except Exception as e:

            # fallback if parsing fails
            return {
                "goal": "Business Setup",
                "workflow": [
                    {
                        "step": 1,
                        "action": llm_output,
                        "authority": "Unknown"
                    }
                ]
            }