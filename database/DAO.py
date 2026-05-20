from database.DB_connect import DBConnect
from model.genere import Genere


class DAO():

    @staticmethod
    def getAllGenres():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                    select *
                    from genre g 
                    """
        cursor.execute(query)
        for row in cursor:
            result.append((row["GenreId"], row["Name"]))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNodes(genereID):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select  a.ArtistId  , a.Name
                    from artist a , album alb, track t 
                    where a.ArtistId =alb.ArtistId 
                    and alb.AlbumId = t.AlbumId 
                    and t.GenreId = %s
                    group by  a.ArtistId  , a.Name 
                        
                        """
        cursor.execute(query, (genereID,))
        for row in cursor:
            result.append((row["ArtistId"], row["Name"]))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAcquistiClienti():
        # =========================================================
        # RESTITUISCE PER OGNI CLIENTE QUALI ARTISTI HA ACQUISTATO
        # ========================================================
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT inv.CustomerId, alb.ArtistId
            FROM invoice inv, invoiceline il, track t, album alb
            WHERE inv.InvoiceId = il.InvoiceId
            AND il.TrackId = t.TrackId
            AND t.AlbumId = alb.AlbumId
            GROUP BY inv.CustomerId, alb.ArtistId

                            """
        cursor.execute(query)
        for row in cursor:
            result.append((row["CustomerId"], row["ArtistId"]))
        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getPopolarità():

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                        select a.ArtistId , sum(i.Quantity) as popolarità 
                        from invoiceline i , track t , album a 
                        where i.TrackId =t.TrackId 
                        and t.AlbumId = a.AlbumId 
                        group by a.ArtistId 
    
                                  """
        cursor.execute(query)
        for row in cursor:
            result.append((row["ArtistId"], row["popolarità"]))
        cursor.close()
        conn.close()
        return result

