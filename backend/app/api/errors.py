DETAIL_PROJECT_NOT_FOUND = "Proyecto no encontrado"
DETAIL_ACTIVITY_NOT_FOUND = "Actividad no encontrada"

NOT_FOUND_PROJECT = {
    404: {"description": DETAIL_PROJECT_NOT_FOUND},
}
NOT_FOUND_ACTIVITY = {
    404: {"description": DETAIL_ACTIVITY_NOT_FOUND},
}
VALIDATION_ERROR = {
    422: {"description": "El cuerpo de la petición no pasó la validación"},
}
