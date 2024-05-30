import re
import pandas as pd
from app import models as m, db
from app.logger import log


def parse_csv(
    products_file: str = "tests/db/Products_Reviews-Products.csv",
    reviews_file: str = "tests/db/Products_Reviews-Reviews.csv",
) -> bool:
    log(log.INFO, "Parsing products file [%s]", products_file)
    product_df = pd.read_csv(products_file)

    def clean_line(line):
        pattern = re.compile(r",(?!\w{10})")
        replacement = ";"
        return re.sub(pattern, replacement, line)

    product_df = product_df.apply(
        lambda x: x.map(clean_line) if x.dtype == "object" else x
    )

    for _, row in product_df.iterrows():
        title = row["Title"].strip()
        asin = row["Asin"].strip()

        # Create and save the Product object
        m.Product(
            title=title,
            asin=asin,
        ).save(False)

    try:
        db.session.commit()
    except Exception as e:
        log(log.ERROR, "Error parsing line [%s]: %s", row, e)
        db.session.rollback()

    reviews_df = pd.read_csv(reviews_file)
    reviews_df = reviews_df.apply(
        lambda x: x.map(clean_line) if x.dtype == "object" else x
    )

    for _, row in reviews_df.iterrows():
        asin = row["Asin"].strip()
        title = row["Title"].strip()
        review = row["Review"].strip()

        product_query = m.Product.select().where(m.Product.asin == asin.strip())
        product: m.Product = db.session.scalar(product_query)
        if product:
            m.Review(
                product=product,
                title=title.strip(),
                review=review.strip(),
            ).save(False)

    try:
        db.session.commit()
    except Exception as e:
        log(log.ERROR, "Error parsing line [%s]: %s", row, e)
        db.session.rollback()

        try:
            db.session.commit()
        except Exception as e:
            log(log.ERROR, "Error parsing line [%s]: %s", row, e)
            db.session.rollback()
            return False

    return True
