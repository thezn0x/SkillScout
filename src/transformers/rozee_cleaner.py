from src.utils.logger import get_logger
from .main_transformer import BaseCleaner
import re
from datetime import datetime, timedelta
from config.settings import TRANSFORMERS
from typing import Dict, Any, Optional

logger = get_logger(__name__)
rozee_cfg = TRANSFORMERS["rozee"]


class RozeeCleaner(BaseCleaner):

    def parse_date(self, date_str: str) -> Optional[str]:
        try:
            if not date_str:
                return None

            date_str = date_str.strip()
            try:
                date_obj = datetime.fromisoformat(date_str)
                return date_obj.isoformat()
            except ValueError:
                pass
            try:
                date_obj = datetime.strptime(date_str, "%b %d, %Y")
                date_obj = date_obj.replace(hour=0, minute=0, second=0, microsecond=0)
                return date_obj.isoformat()
            except ValueError:
                pass
            relative = re.search(
                r'(\d+)\s+(hour|day|week|month)s?\s+ago',
                date_str,
                re.IGNORECASE
            )
            if relative:
                amount = int(relative.group(1))
                unit = relative.group(2).lower().rstrip('s')

                now = datetime.now()
                unit_map = {
                    'hour': timedelta(hours=amount),
                    'day': timedelta(days=amount),
                    'week': timedelta(weeks=amount),
                    'month': timedelta(days=amount * 30)
                }

                if unit in unit_map:
                    date_obj = now - unit_map[unit]
                    date_obj = date_obj.replace(hour=0, minute=0, second=0, microsecond=0)
                    return date_obj.isoformat()

            logger.warning(f"Could not parse Rozee date: {date_str}")
            return None

        except Exception as e:
            logger.error(f"Error parsing Rozee date '{date_str}': {e}")
            return None

    def calculate_apply_before(self, posted_date: Optional[str]) -> Optional[str]:
        if not posted_date:
            return None

        try:
            posted_dt = datetime.fromisoformat(posted_date)
            apply_before_dt = posted_dt + timedelta(days=10)
            return apply_before_dt.isoformat()
        except Exception as e:
            logger.error(f"Error calculating apply_before: {e}")
            return None

    def transform(self, job: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            cleaned = job.copy()
            cleaned = self.clean_basic_fields(cleaned)

            # Salary parsing
            salary = cleaned.get("salary")
            if salary:
                min_sal, max_sal = self.clean_salary(str(salary))
                cleaned["min_salary"] = min_sal
                cleaned["max_salary"] = max_sal
            else:
                cleaned["min_salary"] = None
                cleaned["max_salary"] = None

            # Skills parsing
            skills = cleaned.get("skills")
            if skills:
                if isinstance(skills, str):
                    skills_list = [s.strip() for s in skills.split(',') if s.strip()]
                else:
                    skills_list = skills

                soft_skills, core_skills = self.filter_skills(skills_list)
                cleaned["soft_skills"] = soft_skills
                cleaned["core_skills"] = core_skills
                cleaned["skill_count"] = len(core_skills)
            else:
                cleaned["soft_skills"] = []
                cleaned["core_skills"] = []
                cleaned["skill_count"] = 0

            # Date parsing
            posted_date_str = job.get("posted_date")
            if posted_date_str:
                parsed_date = self.parse_date(str(posted_date_str))
                cleaned["posted_date"] = parsed_date

                if parsed_date:
                    cleaned["apply_before"] = self.calculate_apply_before(parsed_date)
                else:
                    cleaned["apply_before"] = None
            else:
                cleaned["posted_date"] = None
                cleaned["apply_before"] = None

            cleaned["scraped_at"] = datetime.now().isoformat()
            cleaned["source"] = "rozee"

            return cleaned

        except Exception as e:
            logger.error(f"Couldn't transform Rozee job: {e}", exc_info=True)
            return None