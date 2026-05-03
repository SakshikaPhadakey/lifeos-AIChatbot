class ReasoningService:

    def generate_plan(self, business_data):

        if not business_data:
            return {"message": "No information available"}

        business = business_data["business"]
        licenses = business_data["licenses"]
        schemes = business_data["schemes"]

        steps = []

        for license in licenses:
            steps.append(f"Obtain {license}")

        for scheme in schemes:
            steps.append(f"Apply for {scheme}")

        return {
            "goal": f"Start {business}",
            "steps": steps
        }