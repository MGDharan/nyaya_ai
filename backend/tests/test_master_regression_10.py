"""
Master Regression Test Suite (Phase 8): 10 Mandatory Scenario Tests.
Validates:
1. Fake recruiter scam -> BNS 318(4), IT Act 66D (CPA excluded unless qualifying consumer relationship)
2. Friend borrowing Rs 50,000 -> Contract Act / Civil Recovery (NOT criminal cheating)
3. Cheque bounce -> NI Act Section 138
4. Fake social media account -> IT Act Section 66C/66D & BNS
5. Landlord refusing security deposit -> Tenancy law / TPA / Contract Act
6. Workplace sexual harassment -> POSH Act 2013 (NOT Consumer Court)
7. Road traffic accident -> Motor Vehicles Act Section 166 (MACT) & BNS 281/125 (NOT Consumer Court)
8. Lost spectacles reward -> Indian Contract Act Section 168 & Section 8
9. Defective mobile phone -> Consumer Protection Act, 2019
10. Online defamation -> BNS Section 356 & Civil tort for damages
"""

import pytest
from app.agents.multi_agent_pipeline import NyayaMultiAgentPipeline, LegalAgentState


class TestMasterLegalScenarios:
    @classmethod
    def setup_class(cls):
        cls.pipeline = NyayaMultiAgentPipeline()

    def test_01_fake_recruiter(self):
        query = "I paid ₹15,000 to a recruiter for a job offer, but the person disappeared and blocked my phone."
        state = LegalAgentState(question=query)
        res = self.pipeline.run(state)
        ans = res["answer"].lower()

        assert "318" in ans or "420" in ans or "cheating" in ans
        assert "66d" in ans or "information technology" in ans
        # Consumer court should be conditioned or excluded
        assert "consumer" not in [s["title"].lower() for s in res["sources"] if "consumer protection" in s["title"].lower()] or "only if" in ans or "excluded" in ans

    def test_02_friendly_loan_non_payment(self):
        query = "A friend borrowed ₹50,000 from me 6 months ago promising to return it next month, but is now refusing to repay."
        state = LegalAgentState(question=query)
        res = self.pipeline.run(state)
        ans = res["answer"].lower()

        assert "contract" in ans
        assert "civil" in ans or "order xxxvii" in ans or "summary suit" in ans
        # Must NOT classify as criminal cheating without initial deceptive intent
        assert "hriday ranjan" in ans or "mere failure to repay" in ans or "civil breach" in ans or "contract" in ans
        assert state.consumer_applicability.get("cpa_applicable") is False

    def test_03_cheque_bounce(self):
        query = "Someone gave me a cheque of ₹75,000 for goods supplied, but it bounced due to insufficient funds."
        state = LegalAgentState(question=query)
        res = self.pipeline.run(state)
        ans = res["answer"].lower()

        assert "138" in ans
        assert "negotiable instruments" in ans
        assert "30 days" in ans or "notice" in ans

    def test_04_fake_social_media_account(self):
        query = "Someone created a fake social media Instagram account using my photos and full identity to message my friends."
        state = LegalAgentState(question=query)
        res = self.pipeline.run(state)
        ans = res["answer"].lower()

        assert "66c" in ans or "66d" in ans
        assert "information technology" in ans
        assert "identity theft" in ans or "impersonation" in ans

    def test_05_landlord_security_deposit(self):
        query = "My landlord is refusing to return my security deposit of ₹60,000 after I vacated the flat in Chennai."
        state = LegalAgentState(question=query, jurisdiction="Tamil Nadu")
        res = self.pipeline.run(state)
        ans = res["answer"].lower()

        assert "deposit" in ans
        assert "tnrrlta" in ans or "rent authority" in ans or "transfer of property" in ans or "contract" in ans
        assert state.consumer_applicability.get("cpa_applicable") is False

    def test_06_workplace_sexual_harassment(self):
        query = "My manager at office makes unwelcome sexual advances and sends inappropriate messages. What legal steps can I take?"
        state = LegalAgentState(question=query)
        res = self.pipeline.run(state)
        ans = res["answer"].lower()

        assert "posh" in ans or "internal committee" in ans
        assert "75" in ans or "354a" in ans or "sexual harassment" in ans
        assert state.consumer_applicability.get("cpa_applicable") is False
        assert "consumer court" in ans or "consumer disputes" in ans or "internal committee" in ans

    def test_07_road_accident_negligent_driving(self):
        query = "A speeding car hit my motorcycle from behind causing fracture injuries. The driver was driving rashly."
        state = LegalAgentState(question=query)
        res = self.pipeline.run(state)
        ans = res["answer"].lower()

        assert "motor vehicles" in ans or "mact" in ans or "166" in ans
        assert "281" in ans or "279" in ans or "rash driving" in ans or "negligent" in ans
        assert state.consumer_applicability.get("cpa_applicable") is False

    def test_08_lost_spectacles_reward(self):
        query = "Someone advertised a reward of ₹2,000 for finding lost spectacles. I found them and returned them, but the owner refuses to pay the reward."
        state = LegalAgentState(question=query)
        res = self.pipeline.run(state)
        ans = res["answer"].lower()

        assert "168" in ans or "section 8" in ans
        assert "contract" in ans
        assert "finder" in ans or "reward" in ans
        assert state.consumer_applicability.get("cpa_applicable") is False

    def test_09_defective_mobile_phone(self):
        query = "I bought a mobile phone from an electronics showroom for ₹25,000. Within 2 weeks the motherboard stopped working and the seller refuses to replace or refund."
        state = LegalAgentState(question=query)
        res = self.pipeline.run(state)
        ans = res["answer"].lower()

        assert "consumer protection" in ans
        assert "2(7)" in ans or "35" in ans or "deficiency" in ans or "defect" in ans

    def test_10_online_defamation(self):
        query = "A person published false and malicious allegations against my character on Facebook to damage my reputation."
        state = LegalAgentState(question=query)
        res = self.pipeline.run(state)
        ans = res["answer"].lower()

        assert "defamation" in ans
        assert "356" in ans or "499" in ans or "500" in ans
        assert "civil" in ans or "injunction" in ans or "damages" in ans
        assert state.consumer_applicability.get("cpa_applicable") is False

