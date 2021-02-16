--
-- Table structure for `headlines` table
--
DROP TABLE IF EXISTS headlines;

CREATE TABLE headlines (
    id INT NOT NULL AUTO_INCREMENT,
    headline VARCHAR(100) NOT NULL,
    source VARCHAR(100) NOT NULL,
    published_date DATE NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Table structure for `tweets` table
--
DROP TABLE IF EXISTS tweets;

CREATE TABLE tweets (
    id INT NOT NULL AUTO_INCREMENT,
    tweet VARCHAR(255) NOT NULL,
    tweeted_date DATE NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for `cryptos` table
--
DROP TABLE IF EXISTS cryptos;

CREATE TABLE cryptos (
    id INT NOT NULL AUTO_INCREMENT,
    ticker VARCHAR(20) NOT NULL,
    price DECIMAL(16,8) NOT NULL,
    volume DECIMAL(20, 10) NOT NULL,
    updated_at DATE NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
