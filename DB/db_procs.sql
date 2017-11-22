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

DROP PROCEDURE IF EXISTS change_password;

CREATE PROCEDURE change_password(
  p_user_token varchar(15),
  p_new_password varchar(255)
)
  BEGIN
    if valid_token(p_user_token) THEN
      update USERS
      set PASSWORD = p_new_password
      where USER_TOKEN = p_user_token;
      commit;
      if valid_password(
          (select user_name from USERS where user_token = p_user_token),
            p_new_password
      )THEN
        select 1 from dual;
      ELSE
        select -1 from dual;
      END IF;
      else
        select -1 from dual;
    END IF;
  END;

DROP PROCEDURE IF EXISTS create_picture;

CREATE PROCEDURE create_picture(
  p_user_token varchar(15),
  p_food_confidence varchar(20),
  p_not_food_confidence float,
  p_is_food varchar(1)
)
  BEGIN

    if valid_token(p_user_token) THEN

      INSERT INTO PICTURES  (
        USER_ID,
        CREATION_DATE,
        CONFIDENCE_IS_FOOD,
        CONFIDENCE_IS_NOT_FOOD,
        IS_FOOD)
      VALUES (
        (select user_id from USERS where user_token = p_user_token),
        sysdate(),
        p_food_confidence,
        p_not_food_confidence,
        p_is_food_
      );
      COMMIT;

      select USER_ID,PICTURE_ID
      from PICTURES
      where picture_ID = LAST_INSERT_ID();
    ELSE
      select -1 from dual;
    END IF;
  END;

DROP PROCEDURE IF EXISTS create_favorite;

CREATE PROCEDURE create_favorite(
  p_user_token varchar(15),
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
  declare l_token varchar(255);

  if valid_password(p_user_name,p_password) THEN

    select USER_TOKEN
    into l_token
    from USERS
    where USER_NAME = p_user_name;

    if(l_token is null) THEN
      update USERS
      set USER_TOKEN = new_user_token()
      where USER_NAME = p_user_name;

      commit;

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
        AND ifnull(end_date, sysdate() + 1) > sysdate()
    );
  END;

drop function if exists new_user_token;

create function new_user_token() returns varchar(255)
  BEGIN
    DECLARE l_token varchar(255);

    DECLARE valid boolean;

    set valid = false;

    while not valid DO
      set l_token =conv(floor(rand() * 3656158440062975), 10, 36) ;

      set valid = l_token not in(
        select ifnull(user_token,-1) from USERS
      );

    END WHILE;

    return l_token;
  END;

drop PROCEDURE if exists logout;

create PROCEDURE logout(p_user_token varchar(15))

  BEGIN

  if valid_token(p_user_token) THEN

    update USERS
    set user_token = null
    where user_token = p_user_token;

    commit;

    select 1 from dual;

  ELSE

    select -1 from dual;

  END IF;

  END;

drop function if exists valid_token;

create function valid_token(p_token varchar(15)) returns boolean
  BEGIN
    declare valid varchar(1);

    if(p_token is not null) then

      return p_token in(
        select ifnull(user_token,-1) from USERS
      );
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

drop procedure if exists delete_favorite;

create procedure delete_favorite(
  p_user_token varchar(15),
  p_picture_id int)
  BEGIN
    if exists(
      select *
      from FAVORITES
      where
        user_id = (
          select user_id from USERS where user_token = p_user_token
        )
        AND picture_id = p_picture_id
    ) THEN

      delete from FAVORITES
      where picture_id = p_picture_id
      AND  user_id = (
          select user_id from USERS where user_token = p_user_token
      );

      commit;

      select 1 from dual;

    ELSE
      select -1 from dual;
    END IF;
  END;
