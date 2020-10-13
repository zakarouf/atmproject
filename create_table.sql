-- Create TABLE
CREATE TABLE accounts
(	AcctID INT NOT NULL,
	Holder CHAR(64),
	Balance DECIMAL(15,5),
	ACTIVE BOOLEAN,
    PRIMARY KEY (AcctID)
);

CREATE TABLE test_trans
(
	`Date` DATETIME NOT NULL,
	`Remark` CHAR(64),
	`Amount` DECIMAL(15,5),
	`Type` CHAR(3),
	`Balance` DECIMAL(15,5)
)
