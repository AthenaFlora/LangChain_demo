import re
from langchain_core.runnables import RunnableParallel
from typing import Sequence
from models.context import Context
from application.selector.education_selector import EducationSelector
from application.selector.experience_selector import ExperienceSelector
from application.selector.project_selector import ProjectSelector
from application.selector.skill_selector import SkillSelector
from application.selector.summary_selector import SummaryCreator
from application.selector.selector import Selector
from application.template.cv_template import CVTemplate
from models.job import Job
from util.validate import Validate

class CvBuilder:
    def __init__(self, 
                 job: Job, 
                 selectors : Sequence[Selector],
                 context : Context,
                 cv_template : CVTemplate = CVTemplate("app/data/templates/md_template.md")
                 ) -> None:
        self.job = job
        self.selectors = selectors
        self.cv_template = cv_template
        self.context = context
        pass

    async def create_cv_content(self):
        await self._select_content()
        self.cv_template.overwrite_template(self.selected_content)  
    
    def get_cv_text(self) -> str:
        replaced = self.cv_template.get_replaced_text()
        if replaced is None:
            raise Exception("CV is not created yet, call <create_cv_content> first")
        return replaced
    
    def export_cv_md(self) -> str:
        replaced = self.cv_template.get_replaced_text()
        if replaced is None:
            raise Exception("CV is not created yet, call <create_cv_content> first")
        cv_file = "app/data/output/" +Validate.sanitize_filename(f"cv_{self.job.company}_{self.job.title}_{self.context.today}.md").lower()
        with open(cv_file, "w") as f:
            f.write(replaced)
        return cv_file

    async def _select_content(self):
        chains = {}
        create_summary_chain = None
        for selector in self.selectors:
            if not isinstance(selector, SummaryCreator): 
                chains[selector.__class__.__name__] = selector.create_chain()
            else:
                create_summary_chain = selector.create_chain()
        
        select_content_parallel = RunnableParallel(chains)
        self.selected_content = await select_content_parallel.ainvoke({"job_description": self.job.description})
        self._create_summary(create_summary_chain=create_summary_chain)
    
    def _merge_profile(self) -> str | None:
        if self.selected_content is None:
            return None
        profile = ""
        if self.selected_content.__contains__(SkillSelector.__name__):
            profile += f'Skills: {self.selected_content[SkillSelector.__name__]["skills"]} \n'
            profile += '\n'

        if self.selected_content.__contains__(ProjectSelector.__name__):
            profile += 'Projects: \n'
            for v in self.selected_content[ProjectSelector.__name__]["projects"]:
                profile += v.replace("*", "") +'\n'
            profile += '\n'
        
        if self.selected_content.__contains__(ExperienceSelector.__name__):
            profile += 'Experiences: \n'
            for k,v in self.selected_content[ExperienceSelector.__name__]["experiences"].items():
                profile += k + '\n'
                for e in v:
                    profile += e + '\n'
            profile += '\n'
        
        profile += 'Education: \n'
        if self.selected_content.__contains__(EducationSelector.__name__):
            profile += re.sub(r'(&nbsp;|#|\*|\n|left|right|:)', '', self.selected_content[EducationSelector.__name__])
        
        return profile

    def _create_summary(self, create_summary_chain):
        if create_summary_chain is not None:
            merged_profile = self._merge_profile()
            input = {
                "job_description": self.job.description,
                "selected_profile": merged_profile
            }
            if self.selected_content is None:
                self.selected_content = dict()
                self.selected_content[SummaryCreator.__name__] = create_summary_chain.invoke(input)
