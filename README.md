# Password Security Validator

Un outil Python simple pour valider la robustesse des mots de passe selon les bonnes pratiques de cybersécurité.

## Objectif du projet

Projet développé dans le cadre de ma candidature pour le poste d'**Alternant Développeur Cybersécurité Cloud** chez Société Générale.

### Compétences démontrées :
- **Python** : Développement d'outils de sécurité
- **DevSecOps** : Tests automatisés et bonnes pratiques
- **CI/CD** : Pipeline automatisé avec GitHub Actions
- **Sécurité** : Validation et conformité des mots de passe

## Fonctionnalités

- **Validation complète** : Longueur, complexité, mots de passe communs
- **Système de scoring** : Score sur 100 avec recommandations
- **Rapports détaillés** : Export JSON des résultats
- **Interface interactive** : Utilisation en ligne de commande
- **Tests automatisés** : Couverture complète avec pytest
- **Qualité du code** : Linting, formatting, sécurité

## Installation

```bash
# Cloner le projet
git clone https://github.com/votre-username/password-security-validator.git
cd password-security-validator

# Installer les dépendances
pip install -r requirements.txt
```

## Utilisation

### Mode interactif
```bash
python password_validator.py
```

### Utilisation en tant que module Python
```python
from password_validator import PasswordValidator

validator = PasswordValidator()
result = validator.validate_password("MonMotDePasse123!")

print(f"Score: {result['score']}/100")
print(f"Status: {result['status']}")
```

## Exemple de résultat

```json
{
  "password_tested": "******************",
  "score": 95,
  "status": "FORT", 
  "checks": {
    "length": {"passed": true, "points": 20},
    "complexity": {"passed": true, "points": 60},
    "common_password": {"passed": true, "points": 20}
  },
  "recommendations": []
}
```

## Tests

```bash
# Lancer tous les tests
pytest

# Tests avec couverture
pytest --cov=password_validator

# Tests en mode verbose
pytest -v
```

## 🏗️ Structure du projet

```
password-security-validator/
├── password_validator.py      # Script principal
├── tests/
│   └── test_password_validator.py  # Tests unitaires
├── .github/workflows/
│   └── ci.yml                # Pipeline CI/CD
├── requirements.txt          # Dépendances Python
└── README.md                # Documentation
```

## 🔍 Règles de validation

| Critère | Points | Description |
|---------|--------|-------------|
| **Longueur** | 0-20 | 12+ caractères (20pts), 8-11 (10pts), <8 (0pt) |
| **Majuscules** | 15 | Au moins une lettre majuscule |
| **Minuscules** | 15 | Au moins une lettre minuscule |
| **Chiffres** | 15 | Au moins un chiffre |
| **Spéciaux** | 15 | Au moins un caractère spécial |
| **Sécurité** | 20 | Pas dans la liste des mots de passe communs |

### Classification finale :
- **FORT** : 80-100 points
- **MOYEN** : 60-79 points  
- **FAIBLE** : 0-59 points

## 🔄 CI/CD Pipeline

Le projet utilise GitHub Actions pour :
- ✅ Tests automatisés (Python 3.9, 3.10, 3.11)
- ✅ Analyse de couverture de code
- ✅ Scan de sécurité (Bandit, Safety)
- ✅ Contrôle qualité (Black, Flake8, isort)

## 👤 Auteur


### Technologies utilisées
- **Python 3.9+** - Langage principal
- **pytest** - Tests unitaires
- **GitHub Actions** - CI/CD
- **Bandit/Safety** - Sécurité du code

---

