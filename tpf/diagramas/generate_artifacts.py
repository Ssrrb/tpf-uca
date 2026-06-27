#!/usr/bin/env python3
"""Genera los artefactos UML publicables del TPF G11.

La entrada de este script esta limitada a RF/RNF y minutas oficiales del caso.
No incorpora dictamen, defensa ni cierre del TFG.
"""

from __future__ import annotations

from pathlib import Path
import textwrap


ROOT = Path(__file__).resolve().parent
MODELS = ROOT / "overarch" / "models"


CUS = [
    {
        "n": "01",
        "id": "configurar-semestre",
        "title": "Configurar semestre",
        "actor": "Comisión de TFG",
        "actor_alias": "Comision",
        "rf": "RF-01",
        "rnf": "RNF-01, RNF-03",
        "minuta": "Minuta 01",
        "boundary": "IUSemestreTFG",
        "control": "ControlConfiguracionSemestre",
        "entities": ["SemestreTFG", "CronogramaTFG"],
        "fields": ["fechaReunionInicial", "fechaCierreInscripcion", "fechaPublicacionTutores", "fechaLimiteAnteproyecto"],
        "main": "configurarSemestre",
        "normal": [
            "La Comisión solicita configurar el semestre de TFG.",
            "El sistema muestra el formulario de fechas clave.",
            "La Comisión ingresa reunión inicial, cierre de inscripción, publicación de tutores y entrega del anteproyecto.",
            "El sistema valida que las fechas obligatorias estén completas y ordenadas.",
            "El sistema registra el semestre y publica el cronograma inicial.",
        ],
        "alts": ["Si faltan fechas o el orden es inválido, el sistema informa errores y no registra el semestre."],
        "seq_msgs": [
            ("IU", "Control", "configurarSemestre(fechasClave, usuarioActual)", "g11.cu01.control/configurar-semestre"),
            ("Control", "Semestre", "validarFechasClave(fechasClave)", "g11.cu01.semestre/validar-fechas-clave"),
            ("Control", "Semestre", "registrarSemestre(fechasClave, usuarioActual)", "g11.cu01.semestre/registrar-semestre"),
            ("Control", "Cronograma", "publicarCronograma(fechasClave)", "g11.cu01.cronograma/publicar-cronograma"),
            ("IU", "Comision", "mostrarConfirmacion()", "g11.cu01.iu/mostrar-confirmacion"),
        ],
    },
    {
        "n": "02",
        "id": "inscribir-grupo",
        "title": "Inscribir grupo",
        "actor": "Estudiante",
        "actor_alias": "Estudiante",
        "rf": "RF-02, RF-03",
        "rnf": "RNF-02, RNF-04",
        "minuta": "Minuta 02",
        "boundary": "IUInscripcionGrupo",
        "control": "ControlInscripcionGrupo",
        "entities": ["SemestreTFG", "Estudiante", "GrupoTFG"],
        "fields": ["temaTentativo", "integrantes", "medioContacto", "fechaInscripcion"],
        "main": "inscribirGrupo",
        "normal": [
            "El estudiante solicita inscribir su grupo.",
            "El sistema muestra el formulario de inscripción.",
            "El estudiante ingresa tema tentativo, integrantes y medio de contacto.",
            "El sistema valida datos obligatorios, cantidad de integrantes y pertenencia única por semestre.",
            "El sistema registra el grupo y cambia su estado a Inscripto.",
        ],
        "alts": [
            "Si el grupo no tiene entre 1 y 3 integrantes, se informa el error.",
            "Si un estudiante ya pertenece a otro grupo del semestre, se rechaza la inscripción.",
        ],
        "seq_msgs": [
            ("IU", "Control", "inscribirGrupo(temaTentativo, integrantes, medioContacto, usuarioActual)", "g11.cu02.control/inscribir-grupo"),
            ("Control", "Semestre", "obtenerSemestreVigente()", "g11.cu02.semestre/obtener-semestre-vigente"),
            ("Control", "Control", "validarDatosObligatorios(temaTentativo, integrantes, medioContacto)", "g11.cu02.control/validar-datos-obligatorios"),
            ("Control", "Control", "validarCantidadIntegrantes(integrantes)", "g11.cu02.control/validar-cantidad-integrantes"),
            ("Control", "Control", "validarPertenenciaUnica(integrantes, semestre)", "g11.cu02.control/validar-pertenencia-unica"),
            ("Control", "EstudianteEntidad", "perteneceAOtroGrupo(semestre)", "g11.cu02.estudiante/pertenece-a-otro-grupo"),
            ("Control", "Grupo", "registrarInscripcion(temaTentativo, integrantes, medioContacto, semestre, fechaActual, usuarioActual)", "g11.cu02.grupo/registrar-inscripcion"),
            ("Grupo", "Grupo", "cambiarEstado(\"Inscripto\")", "g11.cu02.grupo/cambiar-estado"),
            ("IU", "Estudiante", "mostrarConfirmacionInscripcion(grupoInscripto)", "g11.cu02.iu/mostrar-confirmacion-inscripcion"),
        ],
    },
    {
        "n": "03",
        "id": "consultar-grupos-inscriptos",
        "title": "Consultar grupos inscriptos",
        "actor": "Comisión de TFG",
        "actor_alias": "Comision",
        "rf": "RF-04",
        "rnf": "RNF-06",
        "minuta": "Minuta 03",
        "boundary": "IUConsultaGrupos",
        "control": "ControlConsultaGrupos",
        "entities": ["SemestreTFG", "GrupoTFG"],
        "fields": ["temaTentativo", "cantidadIntegrantes", "estadoCompletitud"],
        "main": "consultarGruposInscriptos",
        "normal": [
            "La Comisión solicita la lista de grupos del semestre.",
            "El sistema verifica el rol de Comisión.",
            "El sistema obtiene los grupos inscriptos.",
            "El sistema calcula completitud, cantidad de integrantes, tema y estado.",
            "El sistema muestra el listado consolidado.",
        ],
        "alts": ["Si el usuario no pertenece a Comisión, se deniega la consulta general."],
        "seq_msgs": [
            ("IU", "Control", "consultarGruposInscriptos(usuarioActual)", "g11.cu03.control/consultar-grupos-inscriptos"),
            ("Control", "Control", "verificarAccesoComision(usuarioActual)", "g11.cu03.control/verificar-acceso-comision"),
            ("Control", "Semestre", "obtenerSemestreVigente()", "g11.cu03.semestre/obtener-semestre-vigente"),
            ("Control", "Grupo", "listarGruposInscriptos(semestre)", "g11.cu03.grupo/listar-grupos-inscriptos"),
            ("Grupo", "Grupo", "calcularCompletitud()", "g11.cu03.grupo/calcular-completitud"),
            ("IU", "Comision", "mostrarListadoGrupos(listado)", "g11.cu03.iu/mostrar-listado-grupos"),
        ],
    },
    {
        "n": "04",
        "id": "asignar-tutor",
        "title": "Asignar tutor",
        "actor": "Comisión de TFG",
        "actor_alias": "Comision",
        "rf": "RF-05",
        "rnf": "RNF-03, RNF-04",
        "minuta": "Minuta 03",
        "boundary": "IUAsignacionTutor",
        "control": "ControlAsignacionTutor",
        "entities": ["SemestreTFG", "GrupoTFG", "Tutor"],
        "fields": ["tutorAsignado", "fechaAsignacion", "usuarioResponsable"],
        "main": "asignarTutor",
        "normal": [
            "La Comisión selecciona un grupo inscripto y un tutor.",
            "El sistema verifica autorización de Comisión.",
            "El sistema valida que la asignación ocurra antes de la fecha de publicación.",
            "El sistema registra tutor, fecha y responsable.",
            "El sistema actualiza el estado del grupo a Tutor asignado.",
        ],
        "alts": [
            "Si el usuario no es Comisión, el sistema deniega la operación.",
            "Si ya pasó la fecha de publicación, el sistema informa que la asignación no corresponde en este flujo.",
        ],
        "seq_msgs": [
            ("IU", "Control", "asignarTutor(grupo, tutor, usuarioActual)", "g11.cu04.control/asignar-tutor"),
            ("Control", "Control", "verificarAutorizacionComision(usuarioActual)", "g11.cu04.control/verificar-autorizacion-comision"),
            ("Control", "Semestre", "validarAntesDePublicacionTutores(fechaActual)", "g11.cu04.semestre/validar-antes-publicacion-tutores"),
            ("Control", "TutorEntidad", "verificarTutorDisponible(tutor)", "g11.cu04.tutor/verificar-tutor-disponible"),
            ("Control", "Grupo", "registrarAsignacionTutor(tutor, fechaActual, usuarioActual)", "g11.cu04.grupo/registrar-asignacion-tutor"),
            ("Grupo", "Grupo", "cambiarEstado(\"Tutor asignado\")", "g11.cu04.grupo/cambiar-estado"),
            ("IU", "Comision", "mostrarAsignacionRegistrada(grupo)", "g11.cu04.iu/mostrar-asignacion-registrada"),
        ],
    },
    {
        "n": "05",
        "id": "publicar-asignacion-tutor",
        "title": "Publicar asignación de tutor",
        "actor": "Comisión de TFG",
        "actor_alias": "Comision",
        "rf": "RF-06",
        "rnf": "RNF-03",
        "minuta": "Minuta 03",
        "boundary": "IUPublicacionTutores",
        "control": "ControlPublicacionTutores",
        "entities": ["SemestreTFG", "GrupoTFG", "Notificacion"],
        "fields": ["fechaPublicacion", "tutorAsignado", "destinatarios"],
        "main": "publicarAsignacionTutor",
        "normal": [
            "La Comisión solicita publicar asignaciones de tutores.",
            "El sistema verifica autorización de Comisión.",
            "El sistema valida que existan grupos con tutor asignado.",
            "El sistema marca las asignaciones como publicadas.",
            "El sistema notifica al grupo correspondiente.",
        ],
        "alts": ["Si un grupo inscripto no tiene tutor asignado, queda fuera de la publicación y se informa a Comisión."],
        "seq_msgs": [
            ("IU", "Control", "publicarAsignaciones(usuarioActual)", "g11.cu05.control/publicar-asignaciones"),
            ("Control", "Control", "verificarAutorizacionComision(usuarioActual)", "g11.cu05.control/verificar-autorizacion-comision"),
            ("Control", "Semestre", "obtenerFechaPublicacionTutores()", "g11.cu05.semestre/obtener-fecha-publicacion-tutores"),
            ("Control", "Grupo", "listarGruposConTutorAsignado()", "g11.cu05.grupo/listar-grupos-con-tutor-asignado"),
            ("Control", "Grupo", "marcarAsignacionPublicada(fechaActual)", "g11.cu05.grupo/marcar-asignacion-publicada"),
            ("Control", "Notificacion", "notificarGrupo(grupo)", "g11.cu05.notificacion/notificar-grupo"),
            ("IU", "Comision", "mostrarPublicacionRealizada()", "g11.cu05.iu/mostrar-publicacion-realizada"),
        ],
    },
    {
        "n": "06",
        "id": "cargar-version-preliminar",
        "title": "Cargar versión preliminar",
        "actor": "Estudiante",
        "actor_alias": "Estudiante",
        "rf": "RF-07",
        "rnf": "RNF-04",
        "minuta": "Minuta 04",
        "boundary": "IUAnteproyectoPreliminar",
        "control": "ControlAnteproyectoPreliminar",
        "entities": ["GrupoTFG", "Anteproyecto"],
        "fields": ["titulo", "problema", "objetivoGeneral", "alcance"],
        "main": "cargarVersionPreliminar",
        "normal": [
            "El estudiante solicita cargar la versión preliminar.",
            "El sistema recupera el grupo del estudiante.",
            "El estudiante ingresa título, problema, objetivo general y alcance.",
            "El sistema valida que los campos mínimos estén completos.",
            "El sistema registra la versión y cambia el estado a En elaboración de anteproyecto.",
        ],
        "alts": ["Si falta alguno de los campos mínimos, el sistema informa errores y conserva el estado anterior."],
        "seq_msgs": [
            ("IU", "Control", "cargarVersionPreliminar(datosAnteproyecto, usuarioActual)", "g11.cu06.control/cargar-version-preliminar"),
            ("Control", "Grupo", "obtenerGrupoDelEstudiante(usuarioActual)", "g11.cu06.grupo/obtener-grupo-del-estudiante"),
            ("Control", "Anteproyecto", "validarDatosMinimos(titulo, problema, objetivoGeneral, alcance)", "g11.cu06.anteproyecto/validar-datos-minimos"),
            ("Control", "Anteproyecto", "registrarVersionPreliminar(datosAnteproyecto, fechaActual, usuarioActual)", "g11.cu06.anteproyecto/registrar-version-preliminar"),
            ("Control", "Grupo", "cambiarEstado(\"En elaboración de anteproyecto\")", "g11.cu06.grupo/cambiar-estado"),
            ("IU", "Estudiante", "mostrarVersionRegistrada()", "g11.cu06.iu/mostrar-version-registrada"),
        ],
    },
    {
        "n": "07",
        "id": "registrar-observaciones",
        "title": "Registrar observaciones",
        "actor": "Tutor",
        "actor_alias": "Tutor",
        "rf": "RF-08",
        "rnf": "RNF-04",
        "minuta": "Minuta 05",
        "boundary": "IUObservacionesTutor",
        "control": "ControlObservacionesTutor",
        "entities": ["GrupoTFG", "Tutor", "Observacion"],
        "fields": ["texto", "fechaRegistro", "responsable"],
        "main": "registrarObservacion",
        "normal": [
            "El tutor selecciona un grupo asignado.",
            "El sistema verifica que el tutor esté asignado al grupo.",
            "El tutor ingresa la observación breve.",
            "El sistema registra observación, fecha y responsable.",
            "El sistema deja la observación disponible para estudiantes y Comisión.",
        ],
        "alts": ["Si el tutor no está asignado al grupo, el sistema deniega el registro."],
        "seq_msgs": [
            ("IU", "Control", "registrarObservacion(grupo, texto, usuarioActual)", "g11.cu07.control/registrar-observacion"),
            ("Control", "TutorEntidad", "verificarTutorAsignado(grupo, usuarioActual)", "g11.cu07.tutor/verificar-tutor-asignado"),
            ("Control", "Grupo", "obtenerAnteproyectoPreliminar()", "g11.cu07.grupo/obtener-anteproyecto-preliminar"),
            ("Control", "Observacion", "registrarObservacion(texto, fechaActual, usuarioActual)", "g11.cu07.observacion/registrar-observacion"),
            ("Control", "Grupo", "agregarObservacion(observacion)", "g11.cu07.grupo/agregar-observacion"),
            ("IU", "Tutor", "mostrarObservacionRegistrada()", "g11.cu07.iu/mostrar-observacion-registrada"),
        ],
    },
    {
        "n": "08",
        "id": "entregar-anteproyecto",
        "title": "Entregar anteproyecto",
        "actor": "Estudiante",
        "actor_alias": "Estudiante",
        "rf": "RF-09, RF-10",
        "rnf": "RNF-04, RNF-05",
        "minuta": "Minuta 06",
        "boundary": "IUEntregaAnteproyecto",
        "control": "ControlEntregaAnteproyecto",
        "entities": ["SemestreTFG", "GrupoTFG", "Anteproyecto", "AutorizacionExcepcional"],
        "fields": ["fechaEntrega", "usuarioResponsable", "autorizacionExcepcional"],
        "main": "entregarAnteproyecto",
        "normal": [
            "El estudiante solicita entregar formalmente el anteproyecto.",
            "El sistema obtiene el grupo y la fecha límite del semestre.",
            "El sistema valida que la entrega esté en plazo o tenga autorización expresa de Comisión.",
            "El sistema registra la entrega formal con fecha y usuario.",
            "El sistema cambia el estado del grupo a Anteproyecto entregado.",
        ],
        "alts": ["Si la fecha límite venció y no existe autorización expresa, el sistema bloquea la entrega."],
        "seq_msgs": [
            ("IU", "Control", "entregarAnteproyecto(archivo, usuarioActual)", "g11.cu08.control/entregar-anteproyecto"),
            ("Control", "Grupo", "obtenerGrupoDelEstudiante(usuarioActual)", "g11.cu08.grupo/obtener-grupo-del-estudiante"),
            ("Control", "Semestre", "obtenerFechaLimiteAnteproyecto()", "g11.cu08.semestre/obtener-fecha-limite-anteproyecto"),
            ("Control", "Autorizacion", "verificarAutorizacionExcepcional(grupo)", "g11.cu08.autorizacion/verificar-autorizacion-excepcional"),
            ("Control", "Control", "validarEntregaHabilitada(fechaActual, fechaLimite, autorizacion)", "g11.cu08.control/validar-entrega-habilitada"),
            ("Control", "Anteproyecto", "registrarEntregaFormal(archivo, fechaActual, usuarioActual)", "g11.cu08.anteproyecto/registrar-entrega-formal"),
            ("Control", "Grupo", "cambiarEstado(\"Anteproyecto entregado\")", "g11.cu08.grupo/cambiar-estado"),
            ("IU", "Estudiante", "mostrarEntregaRegistrada()", "g11.cu08.iu/mostrar-entrega-registrada"),
        ],
    },
    {
        "n": "09",
        "id": "consultar-estado-grupo",
        "title": "Consultar estado del grupo",
        "actor": "Estudiante",
        "actor_alias": "Estudiante",
        "rf": "RF-11",
        "rnf": "RNF-01, RNF-06",
        "minuta": "Minuta 05",
        "boundary": "IUEstadoGrupo",
        "control": "ControlEstadoGrupo",
        "entities": ["SemestreTFG", "GrupoTFG", "Observacion"],
        "fields": ["estado", "tutorAsignado", "fechasClave", "observaciones"],
        "main": "consultarEstadoGrupo",
        "normal": [
            "El estudiante solicita consultar el estado de su grupo.",
            "El sistema obtiene únicamente el grupo asociado al estudiante.",
            "El sistema recupera estado, tutor, fechas clave y observaciones.",
            "El sistema muestra la información del grupo propio.",
        ],
        "alts": ["Si el estudiante no tiene grupo en el semestre, el sistema informa que no existe inscripción asociada."],
        "seq_msgs": [
            ("IU", "Control", "consultarEstadoGrupo(usuarioActual)", "g11.cu09.control/consultar-estado-grupo"),
            ("Control", "Grupo", "obtenerGrupoDelEstudiante(usuarioActual)", "g11.cu09.grupo/obtener-grupo-del-estudiante"),
            ("Control", "Semestre", "obtenerFechasClave()", "g11.cu09.semestre/obtener-fechas-clave"),
            ("Control", "Grupo", "obtenerEstadoYTutor()", "g11.cu09.grupo/obtener-estado-y-tutor"),
            ("Control", "Observacion", "listarObservacionesDelGrupo(grupo)", "g11.cu09.observacion/listar-observaciones-del-grupo"),
            ("IU", "Estudiante", "mostrarEstadoGrupo(resumen)", "g11.cu09.iu/mostrar-estado-grupo"),
        ],
    },
    {
        "n": "10",
        "id": "generar-listado-sin-entrega",
        "title": "Generar listado de grupos sin entrega",
        "actor": "Comisión de TFG",
        "actor_alias": "Comision",
        "rf": "RF-12",
        "rnf": "RNF-06",
        "minuta": "Minuta 06",
        "boundary": "IUListadoSinEntrega",
        "control": "ControlListadoSinEntrega",
        "entities": ["SemestreTFG", "GrupoTFG"],
        "fields": ["fechaLimite", "estadoEntrega", "medioContacto"],
        "main": "generarListadoSinEntrega",
        "normal": [
            "La Comisión solicita el listado de grupos pendientes.",
            "El sistema verifica acceso de Comisión.",
            "El sistema verifica proximidad a la fecha límite.",
            "El sistema selecciona grupos que aún no entregaron anteproyecto.",
            "El sistema muestra el listado para recordatorios.",
        ],
        "alts": ["Si no se está cerca del plazo, el sistema puede mostrar el listado con advertencia de oportunidad."],
        "seq_msgs": [
            ("IU", "Control", "generarListadoSinEntrega(usuarioActual)", "g11.cu10.control/generar-listado-sin-entrega"),
            ("Control", "Control", "verificarAccesoComision(usuarioActual)", "g11.cu10.control/verificar-acceso-comision"),
            ("Control", "Semestre", "verificarProximidadFechaLimite(fechaActual)", "g11.cu10.semestre/verificar-proximidad-fecha-limite"),
            ("Control", "Grupo", "listarGruposSinEntrega()", "g11.cu10.grupo/listar-grupos-sin-entrega"),
            ("IU", "Comision", "mostrarListadoSinEntrega(listado)", "g11.cu10.iu/mostrar-listado-sin-entrega"),
        ],
    },
]


def slug(cu: dict) -> str:
    return f"{cu['n']}-{cu['id']}"


def puml_name(cu: dict, kind: str) -> Path:
    return ROOT / f"{slug(cu)}-{kind}.puml"


def edn_method(ns: str, method_id: str, name: str, typ: str = "void") -> str:
    return f'{{:el :method :id :{ns}/{method_id} :name "{name}" :visibility :public :type "{typ}"}}'


def method_id_from_ref(ref: str) -> tuple[str, str]:
    ns, mid = ref.split("/")
    return ns, mid


def write_bce_model() -> None:
    items: list[str] = [
        ";;;; Modelo BCE consolidado de los diez casos de uso.",
        ";;;; Fuente canonica para operaciones referenciadas por diagramas de secuencia.",
        "",
        "#{",
    ]
    for cu in CUS:
        ns = f"g11.cu{cu['n']}"
        lower_boundary = cu["boundary"][0].lower() + cu["boundary"][1:]
        lower_control = cu["control"][0].lower() + cu["control"][1:]
        items.append(f'  {{:el :package :id :{ns}/frontera :name "Frontera CU-{cu["n"]}"')
        items.append(f'   :ct #{{{{:el :class :id :{ns}/{lower_boundary} :name "{cu["boundary"]}" :stereotype "boundary"')
        b_methods = []
        for _side, _target, msg, ref in cu["seq_msgs"]:
            if ".iu/" in ref:
                ref_ns, mid = method_id_from_ref(ref)
                b_methods.append(edn_method(ref_ns, mid, msg.split("(")[0]))
        if not b_methods:
            b_methods.append(edn_method(f"{ns}.iu", "mostrar-resultado", "mostrarResultado"))
        items.append("          :ct [" + "\n               ".join(b_methods) + "]}}}}")
        items.append("")
        items.append(f'  {{:el :package :id :{ns}/control :name "Control CU-{cu["n"]}"')
        items.append(f'   :ct #{{{{:el :class :id :{ns}/{lower_control} :name "{cu["control"]}" :stereotype "control"')
        c_methods = []
        for _side, _target, msg, ref in cu["seq_msgs"]:
            if ".control/" in ref:
                ref_ns, mid = method_id_from_ref(ref)
                c_methods.append(edn_method(ref_ns, mid, msg.split("(")[0]))
        items.append("          :ct [" + "\n               ".join(dict.fromkeys(c_methods)) + "]}}}}")
        items.append("")
        items.append(f'  {{:el :package :id :{ns}/entidades :name "Entidades CU-{cu["n"]}" :ct #{{')
        alias_to_entity = {
            "Semestre": "SemestreTFG",
            "EstudianteEntidad": "Estudiante",
            "Grupo": "GrupoTFG",
            "TutorEntidad": "Tutor",
            "Cronograma": "CronogramaTFG",
            "Notificacion": "Notificacion",
            "Anteproyecto": "Anteproyecto",
            "Observacion": "Observacion",
            "Autorizacion": "AutorizacionExcepcional",
        }
        for entity in cu["entities"]:
            entity_aliases = [a for a, e in alias_to_entity.items() if e == entity]
            e_methods = []
            for _side, target, msg, ref in cu["seq_msgs"]:
                if target in entity_aliases and ".iu/" not in ref and ".control/" not in ref:
                    ref_ns, mid = method_id_from_ref(ref)
                    e_methods.append(edn_method(ref_ns, mid, msg.split("(")[0]))
            fields = "\n               ".join(
                f'{{:el :field :id :{ns}.{entity.lower()}/{f.lower()} :name "{f}" :visibility :private :type "String"}}'
                for f in cu["fields"][:2]
            )
            class_id = entity[0].lower() + entity[1:]
            items.append(f'         {{:el :class :id :{ns}/{class_id} :name "{entity}" :stereotype "entity"')
            items.append("          :ct [" + fields)
            if e_methods:
                items.append("               " + "\n               ".join(dict.fromkeys(e_methods)))
            items.append("              ]}")
        if cu["n"] == "02":
            items.append('         {:el :enum :id :g11.domain/estado-grupo :name "EstadoGrupo"')
            items.append('          :ct [{:el :enum-value :id :g11.domain.estado/pendiente-inscripcion :name "PENDIENTE_INSCRIPCION"}')
            items.append('               {:el :enum-value :id :g11.domain.estado/inscripto :name "INSCRIPTO"}')
            items.append('               {:el :enum-value :id :g11.domain.estado/tutor-asignado :name "TUTOR_ASIGNADO"}')
            items.append('               {:el :enum-value :id :g11.domain.estado/en-elaboracion :name "EN_ELABORACION_ANTEPROYECTO"}')
            items.append('               {:el :enum-value :id :g11.domain.estado/anteproyecto-entregado :name "ANTEPROYECTO_ENTREGADO"}]}')
        items.append("        }}")
        items.append("")
        items.append(f'  {{:el :dependency :id :{ns}/iu-depende-control :from :{ns}/{lower_boundary} :to :{ns}/{lower_control}}}')
        items.append(f'  {{:el :implements :id :{ns}/control-implementa-cu-{cu["n"]} :from :{ns}/{lower_control} :to :g11.cu/cu-{cu["n"]}-{cu["id"]}}}')
        items.append("")
    items.append("}")
    (MODELS / "20-analisis-bce.edn").write_text("\n".join(items), encoding="utf-8")


def write_views() -> None:
    entries = [
        '  {:el :use-case-view\n   :id :g11.view/casos-de-uso\n   :title "Sistema de gestión de la primera etapa del TFG — Casos de uso"\n   :layout :left-right\n   :selection [{:namespace-prefix "g11.actor"} {:namespace-prefix "g11.cu"}]\n   :include :relations\n   :ct []}'
    ]
    for cu in CUS:
        entries.append(
            f'''  {{:el :code-view
   :id :g11.view/cu-{cu["n"]}-clases-analisis
   :title "CU-{cu["n"]} — {cu["title"]} — Clases de análisis BCE"
   :layout :left-right
   :linetype :orthogonal
   :selection [{{:namespace-prefix "g11.cu{cu["n"]}"}}]
   :include :relations
   :ct []}}'''
        )
    entries.append(
        '''  {:el :state-machine-view
   :id :g11.view/estados-grupo-tfg
   :title "Máquina de estados del Grupo de TFG — Primera etapa — RF-10"
   :layout :left-right
   :include :relations
   :ct [{:ref :g11.state/grupo-tfg}]}'''
    )
    entries.append(
        '''  {:el :model-view
   :id :g11.view/modelo-completo
   :title "Modelo integral G11 — diagnóstico de consistencia"
   :selection {:namespace-prefix "g11"}
   :ct []}'''
    )
    (MODELS / "90-views.edn").write_text(
        ";;;; Vistas derivadas del mismo modelo. Overarch genera PlantUML desde aqui.\n\n#{\n"
        + "\n\n".join(entries)
        + "\n}\n",
        encoding="utf-8",
    )


def write_use_case_diagram() -> None:
    uses = {
        "Estudiante": ["CU-02 Inscribir grupo", "CU-06 Cargar versión preliminar", "CU-08 Entregar anteproyecto", "CU-09 Consultar estado del grupo"],
        "Comision": ["CU-01 Configurar semestre", "CU-03 Consultar grupos inscriptos", "CU-04 Asignar tutor", "CU-05 Publicar asignación de tutor", "CU-10 Generar listado de grupos sin entrega"],
        "Tutor": ["CU-07 Registrar observaciones"],
    }
    lines = [
        "@startuml",
        "!pragma layout smetana",
        "left to right direction",
        "skinparam style strictuml",
        "skinparam shadowing false",
        "title 01 — Diagrama general de casos de uso\\nSistema web de gestión de la primera etapa del TFG",
        'actor "Estudiante" as Estudiante',
        'actor "Comisión de TFG" as Comision',
        'actor "Tutor" as Tutor',
        'actor "Secretaría Académica" as Secretaria',
        'rectangle "Sistema web de gestión de la primera etapa del TFG" {',
    ]
    for cu in CUS:
        lines.append(f'  usecase "{cu["n"]}. {cu["title"]}" as UC{cu["n"]}')
    lines.append("}")
    for actor, names in uses.items():
        for name in names:
            n = name[3:5]
            lines.append(f"{actor} --> UC{n}")
    lines.extend(
        [
            "Secretaria .. UC02 : intervención externa\\ninscripción académica",
            "UC08 ..> UC09 : <<include>>\\nconsultar estado",
            "UC04 ..> UC05 : <<extend>>\\npublicación posterior",
            "legend bottom",
            "Trazabilidad: RF-01..RF-12; RNF-01..RNF-06. Secretaría Académica figura como actor del contexto oficial, sin RF propio de interacción directa.",
            "endlegend",
            "@enduml",
        ]
    )
    (ROOT / "01-casos-de-uso-general.puml").write_text("\n".join(lines), encoding="utf-8")


def write_class_diagram(cu: dict) -> None:
    ent_lines = "\n".join(
        f'class "{e}" as {e} <<entity>> {{\n  - {cu["fields"][0]}: String\n  + consultar(): void\n}}'
        for e in cu["entities"]
    )
    diagram_no = 2 + (int(cu["n"]) - 1) * 2
    puml = f"""@startuml
!pragma layout smetana
left to right direction
skinparam style strictuml
skinparam shadowing false
skinparam classAttributeIconSize 0
title {diagram_no:02d} — CU-{cu["n"]} {cu["title"]}\\nDiagrama de clases de análisis BCE — {cu["rf"]}

class "{cu["boundary"]}" as IU <<boundary>> {{
  + solicitar(): void
  + mostrarResultado(): void
}}

class "{cu["control"]}" as Control <<control>> {{
  + {cu["main"]}(): void
}}

{ent_lines}

IU --> Control
"""
    for e in cu["entities"]:
        puml += f"Control --> {e}\n"
    if "GrupoTFG" in cu["entities"] and "SemestreTFG" in cu["entities"]:
        puml += 'SemestreTFG "1" -- "0..*" GrupoTFG : grupos\n'
    if cu["n"] == "02":
        puml += 'GrupoTFG "1" -- "1..3" Estudiante : integrantes\n'
    if "Tutor" in cu["entities"] and "GrupoTFG" in cu["entities"]:
        puml += 'GrupoTFG "0..*" -- "0..1" Tutor : tutor asignado\n'
    if "Observacion" in cu["entities"] and "GrupoTFG" in cu["entities"]:
        puml += 'GrupoTFG "1" -- "0..*" Observacion : observaciones\n'
    puml += f"""
legend bottom
Trazabilidad: {cu["rf"]}; {cu["rnf"]}; {cu["minuta"]}.
Modelo de análisis BCE sin detalles de implementación.
endlegend
@enduml
"""
    puml_name(cu, "clases-analisis").write_text(puml, encoding="utf-8")


def write_sequence(cu: dict) -> None:
    aliases = {
        "Comision": 'actor "Comisión de TFG" as Comision',
        "Estudiante": 'actor "Estudiante" as Estudiante',
        "Tutor": 'actor "Tutor" as Tutor',
    }
    participants = [
        aliases[cu["actor_alias"]],
        f'boundary ":{cu["boundary"]}" as IU',
        f'control ":{cu["control"]}" as Control',
    ]
    entity_alias = {
        "SemestreTFG": "Semestre",
        "Estudiante": "EstudianteEntidad",
        "GrupoTFG": "Grupo",
        "Tutor": "TutorEntidad",
        "CronogramaTFG": "Cronograma",
        "Notificacion": "Notificacion",
        "Anteproyecto": "Anteproyecto",
        "Observacion": "Observacion",
        "AutorizacionExcepcional": "Autorizacion",
    }
    for e in cu["entities"]:
        participants.append(f'entity ":{e}" as {entity_alias[e]}')
    lines = [
        "@startuml",
        "!pragma layout smetana",
        "skinparam style strictuml",
        "skinparam shadowing false",
        f"title {3 + (int(cu['n']) - 1) * 2:02d} — CU-{cu['n']} {cu['title']}\\nDiagrama de secuencia — {cu['rf']}",
        *participants,
        "",
        f"{cu['actor_alias']} -> IU : solicitar()",
        "activate IU",
    ]
    lines.append(f"IU -> {cu['actor_alias']} : mostrarFormulario()")
    lines.append(f"{cu['actor_alias']} -> IU : ingresarDatos()")
    for idx, (src, dst, msg, ref) in enumerate(cu["seq_msgs"]):
        if idx == 0:
            lines.append(f"IU -> Control : {msg}")
        else:
            lines.append(f"{src} -> {dst} : {msg}")
        lines.append(f"' op: :{ref}")
        if idx == 0:
            lines.append("activate Control")
    lines.extend(
        [
            "alt flujo alternativo o validación incumplida",
            "  Control --> IU : resultadoConErrores",
            f"  IU --> {cu['actor_alias']} : informarSituacion()",
            "else flujo normal",
            "  Control --> IU : resultadoValido",
            f"  IU --> {cu['actor_alias']} : mostrarResultado()",
            "end",
            "deactivate Control",
            "deactivate IU",
            "legend bottom",
            f"Trazabilidad: {cu['rf']}; {cu['rnf']}; {cu['minuta']}.",
            "Cada comentario ' op: referencia una operación del modelo BCE canónico.",
            "endlegend",
            "@enduml",
        ]
    )
    puml_name(cu, "secuencia").write_text("\n".join(lines), encoding="utf-8")


def write_state_diagram() -> None:
    p = """@startuml
!pragma layout smetana
left to right direction
skinparam style strictuml
skinparam shadowing false
title 22 — Diagrama de estados del Grupo TFG\\nRF-10 — primera etapa hasta entrega formal

state "Pendiente de inscripción" as Pendiente
state "Inscripto" as Inscripto
state "Tutor asignado" as TutorAsignado
state "En elaboración de anteproyecto" as Elaboracion
state "¿Entrega habilitada?" as ValidarEntrega <<choice>>
state "Anteproyecto entregado" as Entregado

[*] --> Pendiente : iniciarInscripcion
Pendiente --> Inscripto : inscribirGrupo [datosCompletos and integrantesEntre1y3 and sinDuplicados] / registrarInscripcion
Pendiente --> Pendiente : inscribirGrupo [datosInvalidos or duplicado] / informarErrores
Inscripto --> TutorAsignado : asignarTutor [Comisión and antesPublicacion] / registrarAsignacion
TutorAsignado --> TutorAsignado : publicarAsignacion / notificarGrupo
TutorAsignado --> Elaboracion : cargarVersionPreliminar [datosMinimos] / registrarVersion
Elaboracion --> ValidarEntrega : entregarAnteproyecto
ValidarEntrega --> Entregado : [enPlazo or autorizacionComision] / registrarEntrega
ValidarEntrega --> Elaboracion : [vencido and sinAutorizacion] / rechazarEntrega
Entregado --> [*]

legend bottom
Estados sustantivos definidos por RF-10. No incluye dictamen, defensa ni cierre.
endlegend
@enduml
"""
    (ROOT / "22-estados-grupo-tfg.puml").write_text(p, encoding="utf-8")


def write_persistent_and_er() -> None:
    persistent = """@startuml
!pragma layout smetana
skinparam style strictuml
skinparam shadowing false
skinparam classAttributeIconSize 0
title 23 — Diagrama de clases persistentes\\nPrimera etapa del TFG

class SemestreTFG <<entity>> {
  +id: UUID
  +periodo: String
  +fechaReunionInicial: Date
  +fechaCierreInscripcion: Date
  +fechaPublicacionTutores: Date
  +fechaLimiteAnteproyecto: Date
}
class Estudiante <<entity>> {
  +id: UUID
  +nombre: String
  +correo: String
}
class Tutor <<entity>> {
  +id: UUID
  +nombre: String
  +correo: String
}
class GrupoTFG <<entity>> {
  +id: UUID
  +temaTentativo: String
  +medioContacto: String
  +estado: EstadoGrupo
  +fechaInscripcion: DateTime
}
class Anteproyecto <<entity>> {
  +id: UUID
  +titulo: String
  +problema: Text
  +objetivoGeneral: Text
  +alcance: Text
  +fechaEntrega: DateTime
}
class Observacion <<entity>> {
  +id: UUID
  +texto: Text
  +fechaRegistro: DateTime
  +responsable: String
}
class AutorizacionExcepcional <<entity>> {
  +id: UUID
  +motivo: Text
  +fechaAutorizacion: DateTime
  +responsableComision: String
}
enum EstadoGrupo {
  PENDIENTE_INSCRIPCION
  INSCRIPTO
  TUTOR_ASIGNADO
  EN_ELABORACION_ANTEPROYECTO
  ANTEPROYECTO_ENTREGADO
}

SemestreTFG "1" -- "0..*" GrupoTFG
GrupoTFG "1" -- "1..3" Estudiante : integrantes
GrupoTFG "0..*" -- "0..1" Tutor : tutor
GrupoTFG "1" -- "0..1" Anteproyecto
GrupoTFG "1" -- "0..*" Observacion
GrupoTFG "1" -- "0..1" AutorizacionExcepcional
GrupoTFG --> EstadoGrupo

note bottom
Restricción: un Estudiante no puede integrar más de un GrupoTFG en el mismo SemestreTFG.
end note
@enduml
"""
    (ROOT / "23-clases-persistentes.puml").write_text(persistent, encoding="utf-8")
    er = """@startuml
!pragma layout smetana
hide circle
skinparam linetype ortho
skinparam shadowing false
title 24 — Diagrama entidad-relación\\nPrimera etapa del TFG

entity semestre_tfg {
  * id : uuid <<PK>>
  --
  periodo : varchar
  fecha_reunion_inicial : date
  fecha_cierre_inscripcion : date
  fecha_publicacion_tutores : date
  fecha_limite_anteproyecto : date
}
entity estudiante {
  * id : uuid <<PK>>
  --
  nombre : varchar
  correo : varchar
}
entity tutor {
  * id : uuid <<PK>>
  --
  nombre : varchar
  correo : varchar
}
entity grupo_tfg {
  * id : uuid <<PK>>
  --
  semestre_id : uuid <<FK>>
  tutor_id : uuid <<FK nullable>>
  tema_tentativo : varchar
  medio_contacto : varchar
  estado : varchar
  fecha_inscripcion : timestamp
}
entity grupo_integrante {
  * grupo_id : uuid <<PK,FK>>
  * estudiante_id : uuid <<PK,FK>>
}
entity anteproyecto {
  * id : uuid <<PK>>
  --
  grupo_id : uuid <<FK unique>>
  titulo : varchar
  problema : text
  objetivo_general : text
  alcance : text
  fecha_entrega : timestamp
}
entity observacion {
  * id : uuid <<PK>>
  --
  grupo_id : uuid <<FK>>
  tutor_id : uuid <<FK>>
  texto : text
  fecha_registro : timestamp
  responsable : varchar
}
entity autorizacion_excepcional {
  * id : uuid <<PK>>
  --
  grupo_id : uuid <<FK unique>>
  motivo : text
  fecha_autorizacion : timestamp
  responsable_comision : varchar
}

semestre_tfg ||--o{ grupo_tfg
tutor ||--o{ grupo_tfg
grupo_tfg ||--|{ grupo_integrante
estudiante ||--o{ grupo_integrante
grupo_tfg ||--o| anteproyecto
grupo_tfg ||--o{ observacion
tutor ||--o{ observacion
grupo_tfg ||--o| autorizacion_excepcional

note bottom
Integridad: unique(semestre_id, estudiante_id) se implementa mediante validación sobre grupo_integrante unido a grupo_tfg.
end note
@enduml
"""
    (ROOT / "24-entidad-relacion.puml").write_text(er, encoding="utf-8")


def cleanup_templates() -> None:
    for path in ROOT.glob("template-diagrama-*.*"):
        path.unlink()
    old_partial = MODELS / "20-cu-02-analisis.edn"
    if old_partial.exists():
        old_partial.unlink()


def main() -> None:
    cleanup_templates()
    write_bce_model()
    write_views()
    write_use_case_diagram()
    for cu in CUS:
        write_class_diagram(cu)
        write_sequence(cu)
    write_state_diagram()
    write_persistent_and_er()


if __name__ == "__main__":
    main()
