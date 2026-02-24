type cell = {
    id: string,
    name: string,
    email: string,
    cpf: string,
    rg: string,
    role: string,
    specialization: string[]|string,
    created_at: string,
    password?: string
}

export default cell;