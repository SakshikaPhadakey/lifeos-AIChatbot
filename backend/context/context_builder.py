class ContextBuilder:

    def build_context(self, user_query, graph_data, vector_data):

        context = {
            "user_query": user_query,
            "business": graph_data.get("business"),
            "licenses": graph_data.get("licenses", []),
            "schemes": graph_data.get("schemes", []),
            "knowledge": vector_data
        }

        return context