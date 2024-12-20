from oracleConfig import oracleConfig

class initalBDGeneratorConfigPrueba:    
    @staticmethod
    def iniciaDataBase():
        # Lista de usuarios
        print(f"\033[92minitalBDGeneratorConfigPrueba: Proceso INICIADO\033[0m")
        connection = None
        try:
            connection = oracleConfig.connect()
            cursor = connection.cursor()
            
            drop_commands = [
                # Eliminar tablas
                "BEGIN EXECUTE IMMEDIATE 'DROP TABLE peces_espectaculos_rel CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;",
                "BEGIN EXECUTE IMMEDIATE 'DROP TABLE peces CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;",
                "BEGIN EXECUTE IMMEDIATE 'DROP TABLE espectaculos CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;",

                # Eliminar procedimientos almacenados
                "BEGIN EXECUTE IMMEDIATE 'DROP PROCEDURE peces_PRC_INSERT'; EXCEPTION WHEN OTHERS THEN NULL; END;",
                "BEGIN EXECUTE IMMEDIATE 'DROP PROCEDURE peces_PRC_UPDATE'; EXCEPTION WHEN OTHERS THEN NULL; END;",
                "BEGIN EXECUTE IMMEDIATE 'DROP PROCEDURE peces_PRC_SELECT_ROW'; EXCEPTION WHEN OTHERS THEN NULL; END;",
                
                "BEGIN EXECUTE IMMEDIATE 'DROP PROCEDURE espectaculos_PRC_INSERT'; EXCEPTION WHEN OTHERS THEN NULL; END;",
                "BEGIN EXECUTE IMMEDIATE 'DROP PROCEDURE espectaculos_PRC_UPDATE'; EXCEPTION WHEN OTHERS THEN NULL; END;",
                "BEGIN EXECUTE IMMEDIATE 'DROP PROCEDURE espectaculos_PRC_SELECT_ROW'; EXCEPTION WHEN OTHERS THEN NULL; END;",
                
                "BEGIN EXECUTE IMMEDIATE 'DROP PROCEDURE peces_espectaculos_rel_PRC_INSERT'; EXCEPTION WHEN OTHERS THEN NULL; END;",
                "BEGIN EXECUTE IMMEDIATE 'DROP PROCEDURE peces_espectaculos_rel_PRC_UPDATE'; EXCEPTION WHEN OTHERS THEN NULL; END;",
                "BEGIN EXECUTE IMMEDIATE 'DROP PROCEDURE peces_espectaculos_rel_PRC_SELECT_ROW'; EXCEPTION WHEN OTHERS THEN NULL; END;"
            ]

            create_commands = [
                # Crear la tabla 'peces'
                """
                CREATE TABLE peces (
                    id_pez NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    nombre_pez VARCHAR2(100) NOT NULL,
                    especie_pez VARCHAR2(100) NOT NULL,
                    habilidad VARCHAR2(100) NOT NULL,
                    usuario_creacion VARCHAR2(50) NOT NULL,
                    fecha_creacion DATE NOT NULL,
                    ip VARCHAR2(50) NOT NULL,
                    usuario_modificacion VARCHAR2(50) NOT NULL,
                    fecha_modificacion DATE NOT NULL
                )
                """,
                
                # Crear la tabla 'espectaculos'
                """
                CREATE TABLE espectaculos (
                    id_espectaculo NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    nombre_espectaculo VARCHAR2(100) NOT NULL,
                    descripcion_espectaculo VARCHAR2(255) NOT NULL,
                    fecha_espectaculo DATE NOT NULL,
                    usuario_creacion VARCHAR2(50) NOT NULL,
                    fecha_creacion DATE NOT NULL,
                    ip VARCHAR2(50) NOT NULL,
                    usuario_modificacion VARCHAR2(50) NOT NULL,
                    fecha_modificacion DATE NOT NULL
                )
                """,

                # Crear la tabla 'peces_espectaculos_rel'
                """
                CREATE TABLE peces_espectaculos_rel (
                    id_relacional NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    id_pez NUMBER NOT NULL,
                    id_espectaculo NUMBER NOT NULL,
                    fecha_participacion DATE NOT NULL,
                    usuario_creacion VARCHAR2(50) NOT NULL,
                    fecha_creacion DATE NOT NULL,
                    ip VARCHAR2(50) NOT NULL,
                    usuario_modificacion VARCHAR2(50) NOT NULL,
                    fecha_modificacion DATE NOT NULL,
                    CONSTRAINT fk_pez FOREIGN KEY (id_pez) REFERENCES peces(id_pez),
                    CONSTRAINT fk_espectaculo FOREIGN KEY (id_espectaculo) REFERENCES espectaculos(id_espectaculo)
                )
                """
            ]

            procedures_commands = [
                # Procedimiento 'peces_PRC_INSERT'
                """
                CREATE OR REPLACE PROCEDURE peces_PRC_INSERT (
                    p_nombre_pez IN VARCHAR2,
                    p_especie_pez IN VARCHAR2,
                    p_habilidad IN VARCHAR2,
                    p_usuario_creacion IN VARCHAR2,
                    p_fecha_creacion IN DATE,
                    p_ip IN VARCHAR2,
                    p_usuario_modificacion IN VARCHAR2,
                    p_fecha_modificacion IN DATE,
                    v_salida OUT NUMBER
                ) AS
                BEGIN
                    INSERT INTO peces (
                        nombre_pez, especie_pez, habilidad, usuario_creacion, fecha_creacion, ip, usuario_modificacion, fecha_modificacion
                    ) VALUES (
                        p_nombre_pez, p_especie_pez, p_habilidad, p_usuario_creacion, p_fecha_creacion, p_ip, p_usuario_modificacion, p_fecha_modificacion
                    )
                    RETURNING id_pez INTO v_salida;
                END;
                """,

                # Procedimiento 'peces_PRC_UPDATE'
                """
                CREATE OR REPLACE PROCEDURE peces_PRC_UPDATE (
                    p_id_pez IN NUMBER,
                    p_nombre_pez IN VARCHAR2,
                    p_especie_pez IN VARCHAR2,
                    p_habilidad IN VARCHAR2,
                    p_usuario_creacion IN VARCHAR2,
                    p_fecha_creacion IN DATE,
                    p_ip IN VARCHAR2,
                    p_usuario_modificacion IN VARCHAR2,
                    p_fecha_modificacion IN DATE,
                    v_salida OUT NUMBER
                ) AS
                BEGIN
                    UPDATE peces
                    SET 
                        nombre_pez = p_nombre_pez,
                        especie_pez = p_especie_pez,
                        habilidad = p_habilidad,
                        usuario_creacion = p_usuario_creacion,
                        fecha_creacion = p_fecha_creacion,
                        ip = p_ip,
                        usuario_modificacion = p_usuario_modificacion,
                        fecha_modificacion = p_fecha_modificacion
                    WHERE id_pez = p_id_pez
                    RETURNING id_pez INTO v_salida;
                END;
                """,

                # Procedimiento 'peces_PRC_SELECT_ROW'
                """
                CREATE OR REPLACE PROCEDURE peces_PRC_SELECT_ROW (
                    v_id IN NUMBER,
                    cursor_resultado OUT SYS_REFCURSOR
                ) AS
                BEGIN   
                    OPEN cursor_resultado FOR
                        SELECT id_pez, nombre_pez, especie_pez, habilidad, usuario_creacion, fecha_creacion, ip, usuario_modificacion, fecha_modificacion
                        FROM peces
                        WHERE id_pez = v_id;
                END;
                """,

                # Procedimiento 'espectaculos_PRC_INSERT'
                """
                CREATE OR REPLACE PROCEDURE espectaculos_PRC_INSERT (
                    p_nombre_espectaculo IN VARCHAR2,
                    p_descripcion_espectaculo IN VARCHAR2,
                    p_fecha_espectaculo IN DATE,
                    p_usuario_creacion IN VARCHAR2,
                    p_fecha_creacion IN DATE,
                    p_ip IN VARCHAR2,
                    p_usuario_modificacion IN VARCHAR2,
                    p_fecha_modificacion IN DATE,
                    v_salida OUT NUMBER
                ) AS
                BEGIN
                    INSERT INTO espectaculos (
                        nombre_espectaculo, descripcion_espectaculo, fecha_espectaculo, usuario_creacion, fecha_creacion, ip, usuario_modificacion, fecha_modificacion
                    ) VALUES (
                        p_nombre_espectaculo, p_descripcion_espectaculo, p_fecha_espectaculo, p_usuario_creacion, p_fecha_creacion, p_ip, p_usuario_modificacion, p_fecha_modificacion
                    )
                    RETURNING id_espectaculo INTO v_salida;
                END;
                """,

                # Procedimiento 'espectaculos_PRC_UPDATE'
                """
                CREATE OR REPLACE PROCEDURE espectaculos_PRC_UPDATE (
                    p_id_espectaculo IN NUMBER,
                    p_nombre_espectaculo IN VARCHAR2,
                    p_descripcion_espectaculo IN VARCHAR2,
                    p_fecha_espectaculo IN DATE,
                    p_usuario_creacion IN VARCHAR2,
                    p_fecha_creacion IN DATE,
                    p_ip IN VARCHAR2,
                    p_usuario_modificacion IN VARCHAR2,
                    p_fecha_modificacion IN DATE,
                    v_salida OUT NUMBER
                ) AS
                BEGIN
                    UPDATE espectaculos
                    SET 
                        nombre_espectaculo = p_nombre_espectaculo,
                        descripcion_espectaculo = p_descripcion_espectaculo,
                        fecha_espectaculo = p_fecha_espectaculo,
                        usuario_creacion = p_usuario_creacion,
                        fecha_creacion = p_fecha_creacion,
                        ip = p_ip,
                        usuario_modificacion = p_usuario_modificacion,
                        fecha_modificacion = p_fecha_modificacion
                    WHERE id_espectaculo = p_id_espectaculo
                    RETURNING id_espectaculo INTO v_salida;
                END;
                """,

                # Procedimiento 'espectaculos_PRC_SELECT_ROW'
                """
                CREATE OR REPLACE PROCEDURE espectaculos_PRC_SELECT_ROW (
                    v_id IN NUMBER,
                    cursor_resultado OUT SYS_REFCURSOR
                ) AS
                BEGIN   
                    OPEN cursor_resultado FOR
                        SELECT id_espectaculo, nombre_espectaculo, descripcion_espectaculo, fecha_espectaculo, usuario_creacion, fecha_creacion, ip, usuario_modificacion, fecha_modificacion
                        FROM espectaculos
                        WHERE id_espectaculo = v_id;
                END;
                """,

                # Procedimiento 'peces_espectaculos_rel_PRC_INSERT'
                """
                CREATE OR REPLACE PROCEDURE peces_espectaculos_rel_PRC_INSERT (
                    p_id_pez IN NUMBER,
                    p_id_espectaculo IN NUMBER,
                    p_fecha_participacion IN DATE,
                    p_usuario_creacion IN VARCHAR2,
                    p_fecha_creacion IN DATE,
                    p_ip IN VARCHAR2,
                    p_usuario_modificacion IN VARCHAR2,
                    p_fecha_modificacion IN DATE,
                    v_salida OUT NUMBER
                ) AS
                BEGIN
                    INSERT INTO peces_espectaculos_rel (
                        id_pez, id_espectaculo, fecha_participacion, usuario_creacion, fecha_creacion, ip, usuario_modificacion, fecha_modificacion
                    ) 
                    VALUES (
                        p_id_pez, p_id_espectaculo, p_fecha_participacion, p_usuario_creacion, p_fecha_creacion, p_ip, p_usuario_modificacion, p_fecha_modificacion
                    )
                    RETURNING id_relacional INTO v_salida;
                END;
                """,

                # Procedimiento 'peces_espectaculos_rel_PRC_UPDATE'
                """
                CREATE OR REPLACE PROCEDURE peces_espectaculos_rel_PRC_UPDATE (
                    p_id_relacional IN NUMBER,
                    p_id_pez IN NUMBER,
                    p_id_espectaculo IN NUMBER,
                    p_fecha_participacion IN DATE,
                    p_usuario_creacion IN VARCHAR2,
                    p_fecha_creacion IN DATE,
                    p_ip IN VARCHAR2,
                    p_usuario_modificacion IN VARCHAR2,
                    p_fecha_modificacion IN DATE,
                    v_salida OUT NUMBER
                ) AS
                BEGIN
                    UPDATE peces_espectaculos_rel
                    SET 
                        id_pez = p_id_pez,
                        id_espectaculo = p_id_espectaculo,
                        fecha_participacion = p_fecha_participacion,
                        usuario_creacion = p_usuario_creacion,
                        fecha_creacion = p_fecha_creacion,
                        ip = p_ip,
                        usuario_modificacion = p_usuario_modificacion,
                        fecha_modificacion = p_fecha_modificacion
                    WHERE id_relacional = p_id_relacional
                    RETURNING id_relacional INTO v_salida;
                END;
                """,

                # Procedimiento 'peces_espectaculos_rel_PRC_SELECT_ROW'
                """
                CREATE OR REPLACE PROCEDURE peces_espectaculos_rel_PRC_SELECT_ROW (
                    v_id IN NUMBER,
                    cursor_resultado OUT SYS_REFCURSOR
                ) AS
                BEGIN   
                    OPEN cursor_resultado FOR
                        SELECT id_pez, id_espectaculo, fecha_participacion, usuario_creacion, fecha_creacion, ip, usuario_modificacion, fecha_modificacion
                        FROM peces_espectaculos_rel
                        WHERE id_relacional = v_id;
                END;
                """
            ]

            data_inserts = [
                # Insert en la tabla 'peces'
                "BEGIN peces_PRC_INSERT('Bubbles', 'Pez globo', 'Hacer burbujas', 'admin', SYSDATE, '192.168.1.1', 'admin', SYSDATE, :v_salida); END;",
                "BEGIN peces_PRC_INSERT('Splash', 'Pez payaso', 'Saltar a través de burbujas', 'admin', SYSDATE, '192.168.1.1', 'admin', SYSDATE, :v_salida); END;",
                "BEGIN peces_PRC_INSERT('Glide', 'Pez ángel', 'Deslizarse a través de anillos de burbujas', 'admin', SYSDATE, '192.168.1.1', 'admin', SYSDATE, :v_salida); END;",

                # Insert en la tabla 'espectaculos'
                "BEGIN espectaculos_PRC_INSERT('El Gran Show de Burbujas', 'Espectáculo de burbujas con peces saltadores.', TO_DATE('2024-04-05', 'YYYY-MM-DD'), 'admin', SYSDATE, '192.168.1.1', 'admin', SYSDATE, :v_salida); END;",
                "BEGIN espectaculos_PRC_INSERT('Noche de Burbujeas Acuáticas', 'Espectáculo nocturno de luces y burbujas.', TO_DATE('2024-04-12', 'YYYY-MM-DD'), 'admin', SYSDATE, '192.168.1.1', 'admin', SYSDATE, :v_salida); END;",
                "BEGIN espectaculos_PRC_INSERT('Danza de las Burbujas', 'Danza sincronizada de peces con burbujas flotantes.', TO_DATE('2024-04-15', 'YYYY-MM-DD'), 'admin', SYSDATE, '192.168.1.1', 'admin', SYSDATE, :v_salida); END;",

                # Insert en la tabla 'peces_espectaculos_rel'
                "BEGIN peces_espectaculos_rel_PRC_INSERT(1, 1, SYSDATE, 'admin', SYSDATE, '192.168.1.1', 'admin', SYSDATE, :v_salida); END;",
                "BEGIN peces_espectaculos_rel_PRC_INSERT(2, 2, SYSDATE, 'admin', SYSDATE, '192.168.1.1', 'admin', SYSDATE, :v_salida); END;",
                "BEGIN peces_espectaculos_rel_PRC_INSERT(3, 3, SYSDATE, 'admin', SYSDATE, '192.168.1.1', 'admin', SYSDATE, :v_salida); END;",
                "BEGIN peces_espectaculos_rel_PRC_INSERT(1, 2, SYSDATE, 'admin', SYSDATE, '192.168.1.1', 'admin', SYSDATE, :v_salida); END;",
                "BEGIN peces_espectaculos_rel_PRC_INSERT(2, 3, SYSDATE, 'admin', SYSDATE, '192.168.1.1', 'admin', SYSDATE, :v_salida); END;",
                "BEGIN peces_espectaculos_rel_PRC_INSERT(3, 1, SYSDATE, 'admin', SYSDATE, '192.168.1.1', 'admin', SYSDATE, :v_salida); END;"
            ]

            # Ejecutar los comandos DROP
            for drop in drop_commands:
                try:
                    cursor.execute(drop)
                    print(f"Dropped: Ejecutado correctamente")
                except Exception as e:
                    print(f"Dropped: Error al borrar -> {e}")

            # Ejecutar los comandos CREATE
            for create in create_commands:
                try:
                    cursor.execute(create)
                    print(f"Create: Ejecutado correctamente")
                except Exception as e:
                    print(f"Create: Error al Crear -> {e}")

            # Ejecutar los comandos PRC
            for prc in procedures_commands:
                try:
                    cursor.execute(prc)
                    print(f"PRC: Ejecutado correctamente")
                except Exception as e:
                    print(f"PRC: Error en el PRC -> {e}")
            
            # Ejecutar los comandos INSERT
            for ins in data_inserts:
                try:
                    v_salida = cursor.var(int)  # Crear una variable de salida para recibir el ID generado
                    cursor.execute(ins, v_salida=v_salida)
                    print(f"INSERT: Ejecutado correctamente")
                except Exception as e:
                    print(f"INSERT: Error en el insert -> {e}")

            connection.commit()
            print(f"\033[92minitalBDGeneratorConfigPrueba: Proceso TERMINADO exitosamente\033[0m")
        except Exception as e:
            if connection:  
                connection.rollback()
            raise Exception(f"iniciaDataBase: Error -> {e}")
        finally:
            if connection:
                cursor.close()
                connection.close()  