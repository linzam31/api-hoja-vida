-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 18-11-2026 a las 00:45:45
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `hoja_vida`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cursos`
--

CREATE TABLE `cursos` (
  `id` int(11) NOT NULL,
  `hoja_vida_id` int(11) NOT NULL,
  `nombre` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `cursos`
--

INSERT INTO `cursos` (`id`, `hoja_vida_id`, `nombre`) VALUES
(1, 1, 'Desarrollo Frontend con React'),
(2, 1, 'Bases de Datos Relacionales MySQL'),
(3, 2, 'Backend con Python y Flask'),
(4, 2, 'Control de Versiones con Git y GitHub'),
(5, 3, 'Backend con Python y Flask'),
(6, 3, 'Control de Versiones con Git y GitHub'),
(7, 3, 'Diseño UI/UX en Figma'),
(8, 3, 'Producción Audiovisual y Motion Graphics'),
(9, 5, 'Administración de Servidores Linux'),
(10, 5, 'Fundamentos de Ciberseguridad'),
(11, 6, 'Pruebas de Software y QA'),
(12, 6, 'Desarrollo Móvil con React Native');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estudios`
--

CREATE TABLE `estudios` (
  `id` int(11) NOT NULL,
  `hoja_vida_id` int(11) NOT NULL,
  `nivel` varchar(100) DEFAULT NULL,
  `institucion` varchar(150) DEFAULT NULL,
  `titulo` varchar(150) DEFAULT NULL,
  `anio_graduacion` year(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `estudios`
--

INSERT INTO `estudios` (`id`, `hoja_vida_id`, `nivel`, `institucion`, `titulo`, `anio_graduacion`) VALUES
(1, 1, 'Tecnólogo', 'SENA - Centro de Gestión de Mercados', 'Análisis y Desarrollo de Software', '2026'),
(2, 2, 'Tecnólogo', 'SENA - Complejo Tecnológico', 'Análisis y Desarrollo de Software', '2026'),
(3, 3, 'Tecnólogo', 'SENA - Centro de Diseño Tecnológico Industrial', 'Diseño e Integración de Multimedia', '2025'),
(4, 5, 'Tecnólogo', 'SENA - Centro Industrial y de Aviación', 'Gestión de Redes de Datos', '2025'),
(5, 6, 'Tecnólogo', 'SENA - CENIGRAF', 'Análisis y Desarrollo de Software', '2026');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `experiencias`
--

CREATE TABLE `experiencias` (
  `id` int(11) NOT NULL,
  `hoja_vida_id` int(11) NOT NULL,
  `empresa` varchar(150) NOT NULL,
  `cargo` varchar(100) DEFAULT NULL,
  `tiempo` varchar(100) DEFAULT NULL,
  `funciones` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `experiencias`
--

INSERT INTO `experiencias` (`id`, `hoja_vida_id`, `empresa`, `cargo`, `tiempo`, `funciones`) VALUES
(1, 1, 'Soluciones Digitales Bogotá SAS', 'Desarrolladora Frontend Junior', '8 meses', 'Maquetación de interfaces web responsivas con React y consumo de APIs REST.'),
(2, 2, 'InnovaSoft Medellín', 'Auxiliar de Desarrollo Backend', '1 año', 'Construcción de endpoints en Python, autenticación con JWT y consultas SQL.'),
(3, 3, 'Estudio Creativo Pacífico', 'Diseñadora Multimedia', '10 meses', 'Diseño de prototipos interactivos, identidad visual y piezas gráficas para web.'),
(4, 5, 'Conectividad Caribe SAS', 'Técnico de Soporte y Redes', '1 año y 2 meses', 'Configuración de routers, cableado estructurado y monitoreo de servidores.'),
(5, 6, 'AppFactory Colombia', 'Analista QA y Desarrolladora Móvil', '7 meses', 'Ejecución de pruebas funcionales, reporte de errores y apoyo en vistas móviles.');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `habilidades`
--

CREATE TABLE `habilidades` (
  `id` int(11) NOT NULL,
  `experiencias_id` int(11) NOT NULL,
  `nombre` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `habilidades`
--

INSERT INTO `habilidades` (`id`, `experiencias_id`, `nombre`) VALUES
(1, 1, 'React'),
(2, 1, 'JavaScript'),
(3, 1, 'Trabajo en equipo'),
(4, 2, 'Python'),
(5, 2, 'Flask'),
(6, 2, 'Resolución de problemas'),
(7, 3, 'Figma'),
(8, 3, 'Adobe Illustrator'),
(9, 3, 'Creatividad'),
(10, 4, 'Redes TCP/IP'),
(11, 4, 'Linux'),
(12, 4, 'Comunicación asertiva'),
(13, 5, 'Testing QA'),
(14, 5, 'React Native'),
(15, 5, 'Atención al detalle');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `hojas_vida`
--

CREATE TABLE `hojas_vida` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `edad` int(11) DEFAULT NULL,
  `ciudad` varchar(100) DEFAULT NULL,
  `correo` varchar(150) NOT NULL,
  `fotografia` varchar(255) DEFAULT NULL,
  `programa` varchar(150) DEFAULT NULL,
  `ficha` varchar(20) DEFAULT NULL,
  `jornada` varchar(50) DEFAULT NULL,
  `usuario_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `hojas_vida`
--

INSERT INTO `hojas_vida` (`id`, `nombre`, `edad`, `ciudad`, `correo`, `fotografia`, `programa`, `ficha`, `jornada`, `usuario_id`) VALUES
(1, 'Camila Rodríguez', 20, 'Bogotá', 'camila.rodriguez@gmail.com', 'camila.jpg', 'ADSO', '2875101', 'Diurna', 2),
(2, 'Mateo Fernández', 22, 'Medellín', 'mateo.fernandez@gmail.com', 'mateo.jpg', 'ADSO', '2875102', 'Nocturna', 3),
(3, 'Valeria Morales', 19, 'Cali', 'valeria.morales@gmail.com', 'valeria.jpg', 'Diseño e Integración de Multimedia', '2875103', 'Mixta', 4),
(5, 'Sebastián Castro', 24, 'Barranquilla', 'sebastian.castro@gmail.com', 'sebastian.jpg', 'Gestión de Redes de Datos', '2875104', 'Diurna', 5),
(6, 'Mariana Vargas', 21, 'Bogotá', 'mariana.vargas@gmail.com', 'mariana.jpg', 'ADSO', '2875105', 'Fines de semana', 6);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `correo` varchar(150) NOT NULL,
  `password` varchar(255) NOT NULL,
  `rol` enum('aprendiz','reclutador','administrador') NOT NULL DEFAULT 'aprendiz',
  `estado` tinyint(1) NOT NULL DEFAULT 1,
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `correo`, `password`, `rol`, `estado`, `fecha_creacion`) VALUES
(1, 'Thomas', 'thomas@gmail.com', 'scrypt:32768:8:1$yf9X5xb9gjckooVy$1772117bf0233fcf9c28843ff2976565fc6e348992f1a8d906edcedc99d0eae7c2886e423b359ace18e2eca6b1d114ac3f6b0f734e105884eacf1cca9c38adba', 'reclutador', 1, '2026-11-17 23:03:02'),
(2, 'Camila Rodríguez', 'camila.rodriguez@gmail.com', 'scrypt:32768:8:1$3ljE846GTutuirPe$dbbc1335ca91ef5947d48a369e8598dc4fcba0316b9d85c3c5fabd5a3f32afaef0ee7ca70bd31b27d17b05346df9a5bf9cd5b7465b768e58a3e0511e73639a8f', 'aprendiz', 1, '2026-11-17 23:05:21'),
(3, 'Mateo Fernández', 'mateo.fernandez@gmail.com', 'scrypt:32768:8:1$Ez04fiOnyHsya2TN$adbf9db202501d5793dc6ecce76258c486edb1b45a9aa457a415b12984a96028cdc0ac68cde7b1ca7a34cf88ed45eb86bafc09e3e3afec4370ec50fa85cc340c', 'aprendiz', 1, '2026-11-17 23:08:31'),
(4, 'Valeria Morales', 'valeria.morales@gmail.com', 'scrypt:32768:8:1$cRGfvkzPgfqx9hxB$f82e97aa0054cb8c36a83281d6221ddd749ea422970dfe9a31f09a82a8c9364461c4ffe8371a0d977c6e9f281558e57a044ddcd9c5cfe7ebe2817b928bc8d5ea', 'aprendiz', 1, '2026-11-17 23:11:34'),
(5, 'Sebastián Castro', 'sebastian.castro@gmail.com', 'scrypt:32768:8:1$jKWxfGFnWuWItwDn$d8cc9c563b8c49d9d23d99f5da24eb1c3b744c55709b85f82b91f0b1be586f850b2133ca006bacfa15332ee180cbd4f83cd99118b9a4fad1258897f43c1df054', 'aprendiz', 1, '2026-11-17 23:13:34'),
(6, 'Mariana Vargas', 'mariana.vargas@gmail.com', 'scrypt:32768:8:1$AuUnFV6ozKi6Q2z9$b2efc6aa1b0306861bbaf0ce5c5634542ee1512ab7c3fb5fbd56b1768f98aa8c766c39fdd9529acef7d5e820d04cfe2e5d5af58d06372ff4fbb1aef7d825a130', 'aprendiz', 1, '2026-11-17 23:16:50');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `cursos`
--
ALTER TABLE `cursos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `hoja_vida_id` (`hoja_vida_id`);

--
-- Indices de la tabla `estudios`
--
ALTER TABLE `estudios`
  ADD PRIMARY KEY (`id`),
  ADD KEY `hoja_vida_id` (`hoja_vida_id`);

--
-- Indices de la tabla `experiencias`
--
ALTER TABLE `experiencias`
  ADD PRIMARY KEY (`id`),
  ADD KEY `hoja_vida_id` (`hoja_vida_id`);

--
-- Indices de la tabla `habilidades`
--
ALTER TABLE `habilidades`
  ADD PRIMARY KEY (`id`),
  ADD KEY `experiencias_id` (`experiencias_id`);

--
-- Indices de la tabla `hojas_vida`
--
ALTER TABLE `hojas_vida`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `correo` (`correo`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `cursos`
--
ALTER TABLE `cursos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `estudios`
--
ALTER TABLE `estudios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `experiencias`
--
ALTER TABLE `experiencias`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `habilidades`
--
ALTER TABLE `habilidades`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `hojas_vida`
--
ALTER TABLE `hojas_vida`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `cursos`
--
ALTER TABLE `cursos`
  ADD CONSTRAINT `cursos_ibfk_1` FOREIGN KEY (`hoja_vida_id`) REFERENCES `hojas_vida` (`id`);

--
-- Filtros para la tabla `estudios`
--
ALTER TABLE `estudios`
  ADD CONSTRAINT `estudios_ibfk_1` FOREIGN KEY (`hoja_vida_id`) REFERENCES `hojas_vida` (`id`);

--
-- Filtros para la tabla `experiencias`
--
ALTER TABLE `experiencias`
  ADD CONSTRAINT `experiencias_ibfk_1` FOREIGN KEY (`hoja_vida_id`) REFERENCES `hojas_vida` (`id`);

--
-- Filtros para la tabla `habilidades`
--
ALTER TABLE `habilidades`
  ADD CONSTRAINT `habilidades_ibfk_1` FOREIGN KEY (`experiencias_id`) REFERENCES `experiencias` (`id`);

--
-- Filtros para la tabla `hojas_vida`
--
ALTER TABLE `hojas_vida`
  ADD CONSTRAINT `fk_hoja_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
