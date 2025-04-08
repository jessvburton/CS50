CREATE TABLE stocks(
    user_id INTEGER NOT NULL UNIQUE,
    symbol TEXT NOT NULL,
    name TEXT NOT NULL,
    shares NUMERIC NOT NULL,
    price NUMERIC NOT NULL,
    date TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE transactions(
    user_id INTEGER NOT NULL UNIQUE,
    symbol TEXT NOT NULL,
    name TEXT NOT NULL,
    shares NUMERIC NOT NULL,
    price_per_share NUMERIC NOT NULL,
    total_price NUMERIC NOT NULL,
    transacted NUMERIC NOT NULL,
    date TIMESTAMP
);