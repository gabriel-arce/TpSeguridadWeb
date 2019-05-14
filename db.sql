DROP TABLE IF EXISTS 'tbl_users';
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE 'tbl_users' (
  'user_id' int(5) NOT NULL AUTO_INCREMENT,
  'user_name' varchar(45),
  'user_username' varchar(45),
  'user_password' varchar(45),
  'user_email' varchar(45),
  PRIMARY KEY ('user_id')
);

INSERT INTO 'tbl_users'('user_name', 'user_username', 'user_password', 'user_email') VALUES ('admin', 'Administrador', 'admin', 'admin@example.com');
INSERT INTO 'tbl_users'('user_name', 'user_username', 'user_password', 'user_email') VALUES ('test1', 'Usuario Test', 'inicio123', 'test1@me.com');
INSERT INTO 'tbl_users'('user_name', 'user_username', 'user_password', 'user_email') VALUES ('test2', 'Usuario Test', 'inicio123', 'test2@me.com');
INSERT INTO 'tbl_users'('user_name', 'user_username', 'user_password', 'user_email') VALUES ('test3', 'Usuario Test', 'inicio123', 'test3@me.com');
