from .connection import conn


class BusinessService:

    def get_business_info(self, business_name):

        query = """
        MATCH (b:Business {name:$name})
        OPTIONAL MATCH (b)-[:REQUIRES]->(l:License)
        OPTIONAL MATCH (b)-[:ELIGIBLE_FOR]->(s:Scheme)

        RETURN b.name AS business,
               collect(distinct l.name) AS licenses,
               collect(distinct s.name) AS schemes
        """

        result = conn.run_query(query, {"name": business_name})

        if not result:
            return None

        return result[0]


# simple test
if __name__ == "__main__":

    service = BusinessService()

    data = service.get_business_info("Bakery")

    print(data)