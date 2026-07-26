import re
from typing import Dict, Tuple

class PIIMasker:
    """
    Utilitário para detecção e mascaramento de Dados Pessoais Sensíveis (PII / LGPD).
    Permite sanitizar ou anonimizar currículos antes do envio para modelos ou armazenamento.
    """

    EMAIL_REGEX = r'[\w\.-]+@[\w\.-]+\.\w+'
    PHONE_REGEX = r'(?:\+?55\s*)?(?:\(?\d{2}\)?\s*)?(?:9?\d{4}[-\s]?\d{4})'
    CPF_REGEX = r'\b\d{3}\.\d{3}\.\d{3}-\d{2}\b|\b\d{11}\b'

    @classmethod
    def mask_text(cls, text: str) -> Tuple[str, Dict[str, str]]:
        """
        Substitui emails, telefones e CPFs por placeholders anonimizados.
        Retorna o texto mascarado e um dicionário de mapeamento reverso.
        """
        mapping = {}
        masked_text = text

        # Mascarar Emails
        emails = set(re.findall(cls.EMAIL_REGEX, masked_text))
        for idx, email in enumerate(emails, 1):
            placeholder = f"[EMAIL_PROTEGIDO_{idx}]"
            mapping[placeholder] = email
            masked_text = masked_text.replace(email, placeholder)

        # Mascarar CPFs
        cpfs = set(re.findall(cls.CPF_REGEX, masked_text))
        for idx, cpf in enumerate(cpfs, 1):
            placeholder = f"[CPF_PROTEGIDO_{idx}]"
            mapping[placeholder] = cpf
            masked_text = masked_text.replace(cpf, placeholder)

        # Mascarar Telefones
        phones = set(re.findall(cls.PHONE_REGEX, masked_text))
        for idx, phone in enumerate(phones, 1):
            if len(phone.strip()) >= 8:  # Evita números isolados pequenos
                placeholder = f"[TELEFONE_PROTEGIDO_{idx}]"
                mapping[placeholder] = phone
                masked_text = masked_text.replace(phone, placeholder)

        return masked_text, mapping

    @classmethod
    def unmask_text(cls, text: str, mapping: Dict[str, str]) -> str:
        """
        Restaura as informações originais a partir do dicionário de mapeamento.
        """
        unmasked = text
        for placeholder, original in mapping.items():
            unmasked = unmasked.replace(placeholder, original)
        return unmasked


def mask_sensitive_info(text: str) -> Tuple[str, Dict[str, str]]:
    return PIIMasker.mask_text(text)
