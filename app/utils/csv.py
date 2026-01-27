import csv
from io import StringIO

from app.utils.decorators import static_all_methods


@static_all_methods
class CSV:
    """
    Utility class for generating CSV data using streaming.
    """

    def post_csv_generator(posts):
        """
        Generate CSV rows for Post records.
        """
        yield (
            '"id","title","description","status",'
            '"created_user_id","updated_user_id",'
            '"deleted_user_id","deleted_at","created_at","updated_at"\n'
        )

        for post in posts:
            output = StringIO()
            writer = csv.writer(output, quoting=csv.QUOTE_ALL)

            writer.writerow(
                [
                    post.id,
                    post.title,
                    post.description,
                    post.status,
                    post.create_user_id,
                    post.updated_user_id,
                    post.deleted_user_id,
                    post.deleted_at,
                    post.created_at,
                    post.updated_at,
                ]
            )

            yield output.getvalue()
