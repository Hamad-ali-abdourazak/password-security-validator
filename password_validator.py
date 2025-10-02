#!/usr/bin/env python3

import re
import json
from typing import Dict, List
from datetime import datetime


class PasswordValidator:
    """Validateur de mots de passe selon les bonnes pratiques de sécurité"""
    
    def __init__(self):
        self.common_passwords = [
            "password", "123456", "motdepasse123", "admin", "azerty",
            "bonjour", "salut", "bienvenue", "soleil", "master",
            "password123", "123456789", "qwerty", "abc123", "france",
            "paris", "marseille", "lyon", "bordeaux", "nantes"
        ]
    
    def validate_password(self, password: str) -> Dict:
      
        report = {
            "password_tested": "***" * len(password),  # Masquer le mot de passe
            "timestamp": datetime.now().isoformat(),
            "score": 0,
            "max_score": 100,
            "status": "",
            "checks": {},
            "recommendations": []
        }
        
        # Vérification longueur minimum (20 points)
        if len(password) >= 12:
            report["checks"]["length"] = {"passed": True, "points": 20}
            report["score"] += 20
        elif len(password) >= 8:
            report["checks"]["length"] = {"passed": True, "points": 10}
            report["score"] += 10
        else:
            report["checks"]["length"] = {"passed": False, "points": 0}
            report["recommendations"].append("Utilisez au moins 8 caractères (12+ recommandé)")
        
        # Vérification complexité (60 points total)
        complexity_score = 0
        
        # Majuscules (15 points)
        has_upper = bool(re.search(r'[A-Z]', password))
        if has_upper:
            complexity_score += 15
        else:
            report["recommendations"].append("Ajoutez des lettres majuscules")
        
        # Minuscules (15 points) 
        has_lower = bool(re.search(r'[a-z]', password))
        if has_lower:
            complexity_score += 15
        else:
            report["recommendations"].append("Ajoutez des lettres minuscules")
        
        # Chiffres (15 points)
        has_digit = bool(re.search(r'\d', password))
        if has_digit:
            complexity_score += 15
        else:
            report["recommendations"].append("Ajoutez des chiffres")
        
        # Caractères spéciaux (15 points)
        has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
        if has_special:
            complexity_score += 15
        else:
            report["recommendations"].append("Ajoutez des caractères spéciaux (!@#$%...)")
        
        report["checks"]["complexity"] = {
            "passed": complexity_score >= 45,
            "points": complexity_score,
            "details": {
                "uppercase": has_upper,
                "lowercase": has_lower, 
                "digits": has_digit,
                "special_chars": has_special
            }
        }
        report["score"] += complexity_score
        
        # Vérification mots de passe communs (20 points)
        is_common = password.lower() in self.common_passwords
        if not is_common:
            report["checks"]["common_password"] = {"passed": True, "points": 20}
            report["score"] += 20
        else:
            report["checks"]["common_password"] = {"passed": False, "points": 0}
            report["recommendations"].append("N'utilisez pas de mots de passe communs")
        
        # Déterminer le statut final
        if report["score"] >= 80:
            report["status"] = "FORT"
        elif report["score"] >= 60:
            report["status"] = "MOYEN"
        else:
            report["status"] = "FAIBLE"
        
        return report
    
    def generate_report(self, passwords: List[str]) -> Dict:
        """
        Génère un rapport pour plusieurs mots de passe
        
        Args:
            passwords (List[str]): Liste des mots de passe à tester
            
        Returns:
            Dict: Rapport consolidé
        """
        results = []
        total_score = 0
        
        for i, password in enumerate(passwords, 1):
            result = self.validate_password(password)
            result["password_id"] = f"password_{i}"
            results.append(result)
            total_score += result["score"]
        
        avg_score = total_score / len(passwords) if passwords else 0
        
        return {
            "summary": {
                "total_passwords": len(passwords),
                "average_score": round(avg_score, 2),
                "timestamp": datetime.now().isoformat()
            },
            "results": results
        }


def main():
    """Fonction principale pour utilisation en ligne de commande"""
    print("Password Security Validator")
    print("=" * 40)
    
    validator = PasswordValidator()
    
    # Mode interactif
    while True:
        print("\nOptions:")
        print("1. Tester un mot de passe")
        print("2. Tester plusieurs mots de passe")
        print("3. Quitter")
        
        choice = input("\nChoix (1-3): ").strip()
        
        if choice == "1":
            password = input("Entrez le mot de passe à tester: ")
            result = validator.validate_password(password)
            
            print(f"\nRésultat: {result['status']}")
            print(f"Score: {result['score']}/100")
            
            if result['recommendations']:
                print("\nRecommandations:")
                for rec in result['recommendations']:
                    print(f"  - {rec}")
                    
        elif choice == "2":
            passwords = []
            print("Entrez les mots de passe (tapez 'fin' pour terminer):")
            while True:
                pwd = input("Mot de passe: ")
                if pwd.lower() == 'fin':
                    break
                passwords.append(pwd)
            
            if passwords:
                report = validator.generate_report(passwords)
                print(f"\nScore moyen: {report['summary']['average_score']}/100")
                
                # Sauvegarder le rapport
                with open('password_report.json', 'w', encoding='utf-8') as f:
                    json.dump(report, f, indent=2, ensure_ascii=False)
                print("Rapport sauvegardé dans 'password_report.json'")
                
        elif choice == "3":
            print("Au revoir!")
            break
        else:
            print("Option invalide")


if __name__ == "__main__":
    main()