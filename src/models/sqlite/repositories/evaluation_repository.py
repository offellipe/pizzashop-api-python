from src.models.sqlite.entities.evaluations import Evaluations


class EvaluationRepository:
    def __init__(self, db_connection) -> None:
        self.__db_connection = db_connection

    def get_evaluations(self, restaurant_id: str, offset: int, limit: int):
        try:
            evaluations = (
                self.__db_connection.query(Evaluations)
                .filter(Evaluations.restaurant_id == restaurant_id)
                .order_by(Evaluations.created_at.desc())
                .offset(offset)
                .limit(limit)
                .all()
            )

            return [
                {
                    "id": evaluation.id,
                    "restaurant_id": evaluation.restaurant_id,
                    "created_at": evaluation.created_at,
                    "rating": evaluation.rating,
                    "comment": evaluation.comment,
                    # Adicione outros campos necessários
                }
                for evaluation in evaluations
            ]

        except Exception as e:
            raise Exception(f"Error fetching evaluations: {e}")
