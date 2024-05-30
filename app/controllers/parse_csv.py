import re
import pandas as pd
from app import models as m, db
from app.logger import log


def parse_csv(
    products_file: str = "tests/db/Products_Reviews-Products.csv",
    reviews_file: str = "tests/db/Products_Reviews-Reviews.csv",
) -> bool:
    with open(products_file, "r") as f:
        log(log.INFO, "Parsing products file [%s]", products_file)
        lines = f.readlines()
        for line in lines[1:]:
            log(log.DEBUG, "Parsing line [%s]", line)

            pattern = re.compile(r",(?!\w{10})")
            replacement = ";"
            clear_line = re.sub(pattern, replacement, line)

            title, asin = clear_line.split(",")
            m.Product(
                title=title.strip(),
                asin=asin.strip(),
            ).save(False)

        try:
            db.session.commit()
        except Exception as e:
            log(log.ERROR, "Error parsing line [%s]: %s", line, e)
            db.session.rollback()
            return False

    with open(reviews_file, "r") as f:
        log(log.INFO, "Parsing reviews file [%s]", reviews_file)
        lines = f.readlines()
        for line in lines[1:]:
            log(log.DEBUG, "Parsing line [%s]", line)

            # pattern = re.compile(r",(?!\w{10})")
            # replacement = ";"
            # clear_line = re.sub(pattern, replacement, line)

            asin, title, review = clear_line.split(",")
            product_query = m.Product.select().where(m.Product.asin == asin.strip())
            product: m.Product = db.session.scalar(product_query)
            if product:
                m.Review(
                    product=product,
                    title=title.strip(),
                    review=review.strip(),
                ).save(False)
            else:
                log(log.ERROR, "Product with ASIN [%s] not found", asin)

        try:
            db.session.commit()
        except Exception as e:
            log(log.ERROR, "Error parsing line [%s]: %s", line, e)
            db.session.rollback()
            return False

    return True
