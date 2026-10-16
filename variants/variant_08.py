VARIANT = 23

def script():
    return """
CREATE TABLE product (
    id integer NOT NULL,
    title varchar(200) NOT NULL,
    CONSTRAINT pk_product PRIMARY KEY (id)
);

CREATE TABLE tag (
    id integer NOT NULL,
    name varchar(40) NOT NULL,
    CONSTRAINT pk_tag PRIMARY KEY (id)
);

CREATE TABLE product_tag (
    product_id integer NOT NULL,
    tag_id integer NOT NULL,
    priority smallint NOT NULL DEFAULT 5,
    CONSTRAINT pk_product_tag PRIMARY KEY (product_id, tag_id),
    CONSTRAINT fk_pt_product FOREIGN KEY (product_id) REFERENCES product (id) ON DELETE CASCADE,
    CONSTRAINT fk_pt_tag FOREIGN KEY (tag_id) REFERENCES tag (id) ON DELETE CASCADE,
    CONSTRAINT ck_pt_priority CHECK (priority BETWEEN 1 AND 10)
);

CREATE TABLE category (
    id integer NOT NULL,
    title varchar(100) NOT NULL,
    parent_id integer,
    CONSTRAINT pk_category PRIMARY KEY (id),
    CONSTRAINT fk_category_parent FOREIGN KEY (parent_id) REFERENCES category (id) ON DELETE SET NULL,
    CONSTRAINT ck_category_not_self CHECK (parent_id <> id)
);
"""