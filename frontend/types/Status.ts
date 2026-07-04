export const STEP_MAPPING = {
    "aguardando_triagem": 0,
    "em_triagem_fase_1": 1,
    "em_triagem_fase_2": 2,
    "em_triagem_fase_3": 3,
    "aguardando_medico": 4,
    "em_atendimento": 5,
    "finalizado": 6
}

export type status =  keyof typeof STEP_MAPPING;
export type status_nums = typeof STEP_MAPPING[status]