from database.DB_connect import DBConnect
from model.retailer import Retailer


class DAO():

    @staticmethod
    def getAllNations():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct(country) as nation
                    from go_retailers"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["nation"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct YEAR(`Date`) as year
                    from go_daily_sales"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["year"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(nation):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT gr.*
                    from go_retailers gr 
                    where gr.Country = %s"""

        cursor.execute(query, (nation,))

        for row in cursor:
            result.append(Retailer(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(nation, year, idMapRetailers):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select gds.Retailer_code as ret1, gds2.Retailer_code as ret2, count(distinct gds2.Product_number) as peso
                    from go_daily_sales gds2, go_daily_sales gds, go_retailers gr, go_retailers gr2 
                    where gds.Product_number = gds2.Product_number
                    and gds.Retailer_code < gds2.Retailer_code
                    and gds.Retailer_code = gr.Retailer_code
                    and gds2.Retailer_code = gr2.Retailer_code
                    and gr.Country = gr2.Country
                    and gr2.Country = %s
                    and YEAR(gds.`Date`) = YEAR(gds2.`Date`)
                    and YEAR(gds.`Date`) = %s
                    group by ret1, ret2"""

        cursor.execute(query, (nation, year))

        for row in cursor:
            result.append((idMapRetailers[row["ret1"]], idMapRetailers[row["ret2"]], row["peso"]))

        cursor.close()
        conn.close()
        return result
