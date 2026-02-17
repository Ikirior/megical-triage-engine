from datetime import datetime
import asyncio
from beanie.operators import Or
from fastapi import HTTPException
from models import User, Patient, ServiceSheet
from contracts import (UserCreate, UserResponse, UserUpdate, PatientCreate,
                       PatientUpdate, TriageDataPhaseOne, TriageDataPhaseTwo,
                       TriageDataPhaseThree, TriageInvestigationQA, UnityContextSnapshot, )

# Serviço padrão onde passa o token e o cargo esperado, a função verifica se o token (pode ser um jwt) é válido (não expirou e tem assinatura), se tiver extrai o conteúdo do token e verifica se o row é igual ao enviado no corpo da requisição. Se não passar, dá um unouthorized e passa o que estava esperando.

class UserService:
    """
    Responsável pelo CRUD de funcionários (Admin).
    
    TODO 1: create_user(user_data: UserCreate) -> UserResponse
        - Recebe o schema UserCreate.
        - Verifica se CPF/Email já existem (Regra de Negócio).
        - Hash da senha (usando passlib).
        - Salva no banco.
    
    TODO 2: get_user_by_email(email: str) -> User
        - Será usada pelo AuthService para o Login.
        - Retorna o documento completo (com hash) para verificação interna.
    
    TODO 3: get_user_by_id(user_id: str) -> UserResponse
        - Busca pelo ID para exibir no frontend.
    
    TODO 4: list_users() -> List[UserResponse]
        - Retorna todos os funcionários para o painel do Admin.
    
    TODO 5: update_user(user_id: str, new_data: UserUpdate) -> UserResponse
        - Atualiza campos parciais.
        - se tiver uma senha nova, refaz o hash antes de salvar.
    
    TODO 6: delete_user(user_id: str) -> bool
        - Se um funcionário for demitido, o Admin tem que remover o acesso.
    """
    async def create_user(user_data: UserCreate) -> UserResponse:
        
        find_exist_user = await User.find_one(Or(user_data.email == UserCreate.email, user_data.cpf == UserCreate.cpf))
        
        if find_exist_user:
            raise HTTPException(status_code=400, detail="Usuário já cadastrado.")
        
        password_hash = AuthService.get_password_hash(user_data.password)
            
        new_user = User(
            **user_data.model_dump(exclude={"password"}),
            password_hash=password_hash
        )
        
        await new_user.insert()
        
        return UserResponse(**new_user.model_dump())
    pass

class PatientService:
    """
    Responsável pelo ciclo de vida do Paciente e Check-in.
    
    TODO 1: get_patient_by_cpf(cpf: str) -> Optional[Patient]
        - Usado pela recepção para buscar cadastro.
        - Se encontrar, retorna o objeto Patient.
        - Se não, retorna None (sinal para abrir formulário de cadastro).
    
    TODO 2: create_patient(data: PatientCreate) -> Patient
        - Cria o registro demográfico no banco.
        - Valida duplicidade de CPF (caso a busca anterior falhe).
    
    TODO 3: update_patient(patient_id: PydanticObjectId, data: PatientUpdate) -> Patient
        - Caso o paciente mudou de endereço ou telefone.
    
    TODO 4: _get_patient_history_context(patient_id: str) -> List[PatientHistoryItem]
        - A memória do MedGemma sobre o paciente.
        - Busca no banco 'ServiceSheets' onde status="finalizado" E patient_ref=patient_id.
        - Ordena por data (decrescente).
        - Limita a 5.
        - Retorna um JSON simplificado com todos os 5 últimos objetos 
        - Isso será injetado no prompt da IA depois.
    
    TODO 5: check_in_patient(patient_id: str, receptionist_id: str) -> ServiceSheet
        - Ação de "Entrada na Fila".
        - Cria uma nova ServiceSheet.
        - Define status = "aguardando_triagem".
        - Vincula o ID do paciente e o ID da recepcionista.
        - Não preenche dados médicos ainda.
    """
    pass

class TriageService:
    """
    Orquestrador da Triagem. Gerencia o fluxo: Dados -> IA -> Banco.
    
    Dependências:
    - PatientService
    - MedGemmaProvider
    
    TODO 1: get_triage_queue() -> List[TriageQueueItem]
        - Busca no banco ServiceSheets onde status == "aguardando_triagem".
        - IMPORTANTE: Não trazer status "em_triagem" ou "finalizado".
        - Deve usar fetch_links=True para acessar o nome do paciente (ServiceSheet.patient_ref.name).
        - Ordena por created_at - Quem chegou primeiro é atendido primeiro (First In - First Out
        - Retorna uma lista simplificada apenas para exibição no painel.

    TODO 2: _calculate_unit_context() -> UnityContextSnapshot
        - Método interno.
        - Conta quantos documentos 'ServiceSheet' existem com status "aguardando_triagem" ou "em_analise_ia".
        - Se count < 10: "low", < 20: "medium", etc.
        - Retorna o objeto UnityContextSnapshot com o timestamp atual.
    
    TODO 3: start_triage(sheet_id: PydanticObjectId, nurse_id: PydanticObjectId) -> ServiceSheetDetail
        - Quando o enfermeiro clica no card da fila.
        - Verifica se a ficha existe e está livre
        - Muda status de "aguardando_triagem" para "em_triagem".
        - Vincula o nurse_ref - Isso impede que outro enfermeiro pegue o mesmo paciente.
        - Salva no Banco
        - Retorna o objeto ServiceSheetDetail populado
    
    TODO 4: execute_phase_one(sheet_id: PydanticObjectId, input_data: TriageDataPhaseOne) -> List[TriageInvestigationQA]
        - Busca a ServiceSheet pelo ID.
        - Salva Vitals e Observações Iniciais no 'triage_data'.
        - Chama PatientService._get_patient_history_context() para pegar o histórico.
        - Chama _calculate_unit_context() para pegar o contexto da unidade (lotação).
        - Chama MedGemmaProvider.orchestrate_investigation(input_data, history, unit_context).
        - Salva as perguntas geradas no banco.
        - Retorna List[TriageInvestigationQA] para o Frontend.
    
    TODO 5: execute_phase_two(sheet_id: PydanticObjectId, input_data: TriageDataPhaseTwo) -> str
        - Busca a ServiceSheet.
        - Salva as respostas (investigation_qa) enviadas pelo enfermeiro.
        - Recupera as informações de Vitals + Observações
        - Chama PatientService._get_patient_history_context() para pegar o histórico.
        - Chama _calculate_unit_context() para pegar o contexto da unidade (lotação).
        - Chama MedGemmaProvider.generate_medical_suggestion(triage_data, history_context, unit_context). No contexto completo
        - Salva a sugestão ai_generated_suggestion no banco.
        - Retorna a string da sugestão.
    
    TODO 6: execute_phase_three(sheet_id: PydanticObjectId, input_data: TriageDataPhaseThree) -> bool
        - Busca a ServiceSheet.
        - Salva a classificação de risco e notas finais do enfermeiro.
        - Atualiza status para "aguardando_medico".
        - (Opcional/Async) Dispara MedGemmaProvider.generate_doctor_summary().
        - Retorna True (Sucesso).
    """
    pass

class DoctorService:
    """
    Gestão do atendimento médico e fila de espera inteligente.
    
    TODO 1: get_doctor_queue() -> List[DoctorQueueItem]
        - Busca ServiceSheets com status="aguardando_medico".
        - Regra de priorização:
            1. Ordena pela cor de risco (Vermelho > Laranja > Amarelo > Verde > Azul).
            2. Desempate: Quem chegou primeiro (created_at ou updated_at mais antigo).
        - Retorna a lista ordenada para o médico chamar o próximo.

    TODO 2: start_consultation(sheet_id: PydanticObjectId, doctor_id: PydanticObjectId) -> ServiceSheetDetail
        - Quando o médico clica em um paciente da fila.
        - Retorna a ficha completa (com vitais, histórico, resumo da IA pré-consulta).
        - (Opcional) Pode mudar o status para "em_atendimento" aqui se quiser travar o paciente para outros médicos não chamarem.

    TODO 3: finish_consultation(sheet_id: PydanticObjectId, input_data: DoctorData: PydanticObjectId) -> ServiceSheetDetail
        - Recebe o input do médico (Diagnóstico, Prescrição, Notas).
        - Atualiza 'doctor_data' na ServiceSheet.
        - Define 'doctor_ref' = doctor_id.
        - Define status = "finalizado".
        - Salva e retira o paciente da fila.
    """
    pass

class MedGemmaProvider:
    """
    Encapsula o Agente MedGemma e atua como um provedor de sugestões.
    
    TODO 1: orchestrate_investigation(actual_triage: TriageDataPhaseOne) -> List[TriageInvestigationQA]
        - MÉTODO PÚBLICO (Usado na Fase 1).
        - Atua como o decisor.
        - Gera o histórico do paciente List[TriageQueueItem] chamando _get_patient_history_context()
        - Gera o status atual da unidade de saúde UnityContextSnapshot chamando _calculate_unit_context()
        - Passo 1: Chama _decide_investigation_need().
        - Se a decisão for não perguntar: Retorna lista vazia [].
        - Se a decisão for perguntar: Chama _generate_questions() passando a quantidade decidida.
        - Retorna a lista de objetos TriageInvestigationQA.

    TODO 2: _decide_investigation_need(context_data) -> Dict
        - MÉTODO PRIVADO (Interno do Agente).
        - Analisa a entropia/incerteza do caso.
        - Prompt focada em raciocínio clínico
        - Retorna: {"needs_investigation": bool, "num_questions": int, "reasoning": str}

    TODO 3: _generate_questions(context_data, num_questions: int) -> List[TriageInvestigationQA]
        - MÉTODO PRIVADO (Interno do Agente).
        - Só é chamado se o TODO 2 for True.
        - Gera as perguntas específicas baseadas no raciocínio anterior.
        - Garante que a saída esteja no formato JSON estrito para virar objeto Pydantic.

    TODO 4: generate_medical_suggestion(vitals, obs, history, qa_answers: List[TriageInvestigationQA]) -> str
        - MÉTODO PÚBLICO (Usado na Fase 2).
        - Compila todo o contexto + as respostas que o paciente deu.
        - Gera um texto técnico em bullet points (seguindo a lógica Médico para Enfermeiro) sugerindo a hipótese diagnóstica e pontos de atenção. São sugestões e podem ser modificadas.

    TODO 5: generate_doctor_summary(sheet: ServiceSheet) -> str
        - MÉTODO PÚBLICO (Usado na Fase 3 e na fila de maneira assíncrona).
        - Gera o resumo técnico para o médico.
        - Resume o caso focando no auxílo à tomada de decisão rápida.
    """
    pass

class AuthService:
    """
    Gestão de Segurança, Criptografia e Tokens JWT.
    
    Dependências:
    - UserService (para buscar o usuário no banco pelo email)
    
    TODO 1: _get_password_hash(password: str) -> str
        - Função utilitária de Hash.
        - Recebe a senha crua ("123456") e retorna o hash ("$2b$12$...").
        - Usada pelo UserService.create_user().
    
    TODO 2: _verify_password(plain_password: str, hashed_password: str) -> bool
        - Função utilitária de Verificação.
        - Compara a senha crua enviada no login com o hash salvo no banco.
        - Retorna True/False.
    
    TODO 3: authenticate_user(email: str, password: str) -> Optional[str] = False
        - A Lógica de Login propriamente dita.
        - 1. Chama UserService.get_user_by_email(email).
        - 2. Se usuário não existir -> Retorna False.
        - 3. Chama self.verify_password(password, user.password_hash).
        - 4. Se senha não bater -> Retorna False.
        - 5. Retorna o objeto User se tudo estiver OK.
    
    TODO 4: create_access_token(data: dict, expires_delta: timedelta = None) -> str
        - Cria o Token JWT assinado.
        - Recebe os dados do usuário (sub=user_id, role=user_role).
        - Define o tempo de expiração.
        - Retorna a string do token.
    
    TODO 5: decode_access_token(token: str) -> dict
        - Decodifica e valida o Token.
        - Usado pelas Dependências de Rota para saber se o usuário está logado.
        - Retorna os dados do usuário em um payload ou lança erro se o token estiver expirado/inválido.
    """
    
    def get_password_hash(password: str) -> str:
        pass
    pass