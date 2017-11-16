DROP PROCEDURE IF EXISTS create_user;

CREATE PROCEDURE create_user(
  p_user_name varchar(30),
  p_password varchar(255)
)
  begin
    if not (valid_user(p_user_name)) THEN

      insert into USERS(USER_NAME,PASSWORD,CREATION_DATE)
      VALUES(p_user_name,p_password,sysdate());

      commit;

      SELECT LAST_INSERT_ID() as 'user_id';

    ELSE

      select -1 from dual;

    END IF;

  END;

DROP PROCEDURE IF EXISTS create_picture;

CREATE PROCEDURE create_picture(
  p_user_token  int,
  p_analysis varchar(20),
  p_confidence float
)
  BEGIN

    if valid_token(p_user_token) THEN

      INSERT INTO PICTURES  (
        USER_ID,
        CREATION_DATE,
        ANALYSIS,
        CONFIDENCE)
      VALUES (
        (select user_id from USERS where user_token = p_user_token),
        sysdate(),
        p_analysis,
        p_confidence
      );
      COMMIT;

      SELECT LAST_INSERT_ID() as 'picture_id';
    ELSE
      select -1 from dual;
    END IF;
  END;

DROP PROCEDURE IF EXISTS create_favorite;

CREATE PROCEDURE create_favorite(
  p_user_token int,
  p_picture_id int
)
  BEGIN

if valid_token(p_user_token)
    AND valid_picture(p_picture_id)
    AND not in_favorites(
      (select user_id from USERS where user_token = p_user_token),
      p_picture_id
   )THEN


    insert into FAVORITES (
      USER_ID,
      PICTURE_ID,
      CREATION_DATE)
    VALUES(
      (select user_id from USERS where user_token = p_user_token),
      p_picture_id,
      sysdate()
    );

      commit;
      SELECT LAST_INSERT_ID() as 'favorite_id';
    ELSE
      select -1 from dual;
end if;
  END;

DROP PROCEDURE IF EXISTS login;

CREATE PROCEDURE login(
  p_user_name VARCHAR(30),
  p_password  VARCHAR(255)
)
BEGIN
  declare l_token int;

  if valid_password(p_user_name,p_password) THEN

    select USER_TOKEN
    into l_token
    from USERS
    where USER_NAME = p_user_name;

    if(l_token is null) THEN
      update USERS
      set USER_TOKEN = new_user_token()
      where USER_NAME = p_user_name;

    END IF;

    select USER_TOKEN from USERS where user_name = p_user_name;
  ELSE

    select -1 from dual;

  END IF;

END;

DROP FUNCTION IF EXISTS valid_user;

Create FUNCTION valid_user(
  p_user_name varchar(30)) returns boolean
  BEGIN
    return exists(
       select user_name from USERS WHERE
          user_name = p_user_name
    );
  END;

drop function if exists new_user_token;

create function new_user_token() returns int
  BEGIN
    DECLARE l_token int;
    DECLARE valid varchar(1);
    select floor (rand() * (2147483647 - 1000000000) + 1000000000) into l_token;

    select if(l_token in(
      select user_token from USERS
    ),'N','Y')
    into valid;

    while valid <> 'Y' DO
      select floor (rand() * (2147483647 - 1000000000) + 1000000000) into l_token;

      select if(l_token in(
        select user_token from USERS
      ),'N','Y')
      into valid;

    END WHILE;

    return l_token;
  END;

drop function if exists logout;

create function logout(p_user_token  int) returns boolean

  BEGIN

  update USERS
  set user_token = null
  where user_token = p_user_token;

  return true;

  END;

drop function if exists valid_token;

create function valid_token(p_token int) returns boolean
  BEGIN
    declare valid varchar(1);

    if(p_token is not null) then

      select if(p_token in(
      select user_token from USERS
    ),'Y','N')
      into valid;

      if valid = 'Y' THEN
        return true;
      END IF;
    end if;
    return false;
  END;

drop function if exists valid_picture;

CREATE function valid_picture(p_picture_id int)
  returns BOOLEAN
  BEGIN
    declare valid varchar(1);

    select if(p_picture_id in(
      select PICTURE_ID from PICTURES
    ),'Y','N')
    into valid;

    if valid = 'Y' THEN
      return true;
    END IF;
      return false;
  END;

drop function if exists valid_password;

create function valid_password(p_user_name varchar(30),p_password varchar(255))
  returns BOOLEAN
  BEGIN
    if (valid_user(p_user_name)) then

      return exists(
        select * from USERS
        where user_name = p_user_name
        AND PASSWORD = p_password
      );

    ELSE
      return false;
    end if;
  END;

drop function if EXISTS in_favorites;

create function in_favorites(p_user_id int, p_picture_id  int) returns boolean

  BEGIN
      return exists(
        select *
        from FAVORITES
        where user_id = p_user_id
        AND picture_id = p_picture_id
      );
  END;

drop function IF EXISTS disable_user;
