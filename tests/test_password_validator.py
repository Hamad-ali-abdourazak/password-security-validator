#!/usr/bin/env python3
"""
Tests unitaires pour Password Security Validator
"""

import pytest
import sys
import os

# Ajouter le répertoire parent au path pour importer le module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from password_validator import PasswordValidator


class TestPasswordValidator:
    """Tests pour la classe PasswordValidator"""
    
    def setup_method(self):
        """Initialise le validateur avant chaque test"""
        self.validator = PasswordValidator()
    
    def test_strong_password(self):
        """Test avec un mot de passe fort"""
        password = "MonMotDePasse123!"
        result = self.validator.validate_password(password)
        
        assert result["status"] == "FORT"
        assert result["score"] >= 80
        assert result["checks"]["length"]["passed"] == True
        assert result["checks"]["complexity"]["passed"] == True
        assert result["checks"]["common_password"]["passed"] == True
    
    def test_weak_password(self):
        """Test avec un mot de passe faible"""
        password = "123"
        result = self.validator.validate_password(password)
        
        assert result["status"] == "FAIBLE"
        assert result["score"] < 60
        assert result["checks"]["length"]["passed"] == False
        assert len(result["recommendations"]) > 0
    
    def test_common_password(self):
        """Test avec un mot de passe commun"""
        password = "password"
        result = self.validator.validate_password(password)
        
        assert result["checks"]["common_password"]["passed"] == False
        assert "mots de passe communs" in str(result["recommendations"])
    
    def test_medium_password(self):
        """Test avec un mot de passe moyen"""
        password = "MonMotDePasse"  # Pas de chiffres ni caractères spéciaux
        result = self.validator.validate_password(password)
        
        assert result["status"] in ["MOYEN", "FAIBLE"]
        assert 20 <= result["score"] < 80
    
    def test_complexity_requirements(self):
        """Test des exigences de complexité"""
        # Test majuscules
        result = self.validator.validate_password("PASSWORD123!")
        assert result["checks"]["complexity"]["details"]["uppercase"] == True
        
        # Test minuscules  
        result = self.validator.validate_password("password123!")
        assert result["checks"]["complexity"]["details"]["lowercase"] == True
        
        # Test chiffres
        result = self.validator.validate_password("Password123!")
        assert result["checks"]["complexity"]["details"]["digits"] == True
        
        # Test caractères spéciaux
        result = self.validator.validate_password("Password123!")
        assert result["checks"]["complexity"]["details"]["special_chars"] == True
    
    def test_length_scoring(self):
        """Test du système de scoring par longueur"""
        # Mot de passe court (< 8 caractères)
        short_result = self.validator.validate_password("Ab1!")
        assert short_result["checks"]["length"]["points"] == 0
        
        # Mot de passe moyen (8-11 caractères)
        medium_result = self.validator.validate_password("Password1!")
        assert medium_result["checks"]["length"]["points"] == 10
        
        # Mot de passe long (12+ caractères)
        long_result = self.validator.validate_password("MonLongPassword1!")
        assert long_result["checks"]["length"]["points"] == 20
    
    def test_generate_report(self):
        """Test de la génération de rapport pour plusieurs mots de passe"""
        passwords = ["Password123!", "weak", "VeryStrongPassword2024!"]
        report = self.validator.generate_report(passwords)
        
        assert report["summary"]["total_passwords"] == 3
        assert len(report["results"]) == 3
        assert "average_score" in report["summary"]
        assert report["summary"]["average_score"] >= 0
        
        # Vérifier que chaque résultat a un ID unique
        ids = [result["password_id"] for result in report["results"]]
        assert len(set(ids)) == 3  # Tous les IDs sont uniques
    
    def test_empty_password(self):
        """Test avec un mot de passe vide"""
        result = self.validator.validate_password("")
        
        assert result["status"] == "FAIBLE"
        assert result["score"] == 0
        assert result["checks"]["length"]["passed"] == False
    
    def test_password_masking(self):
        """Test que le mot de passe est masqué dans le rapport"""
        password = "TestPassword123!"
        result = self.validator.validate_password(password)
        
        # Le mot de passe ne doit pas apparaître en clair
        assert password not in str(result)
        assert result["password_tested"] == "***" * len(password)
    
    def test_recommendations_generation(self):
        """Test de la génération des recommandations"""
        # Mot de passe sans majuscules
        result = self.validator.validate_password("password123!")
        recommendations = result["recommendations"]
        assert any("majuscules" in rec for rec in recommendations)
        
        # Mot de passe sans caractères spéciaux
        result = self.validator.validate_password("Password123")
        recommendations = result["recommendations"]
        assert any("spéciaux" in rec for rec in recommendations)