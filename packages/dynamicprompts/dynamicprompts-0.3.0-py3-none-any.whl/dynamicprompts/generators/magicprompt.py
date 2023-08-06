from __future__ import annotations

import logging
from typing import List

from .promptgenerator import PromptGenerator
from dynamicprompts.generators import DummyGenerator
import re

from tqdm import trange

logger = logging.getLogger(__name__)

try:
    from transformers import set_seed
    from transformers import AutoTokenizer, AutoModelForCausalLM
    from transformers import pipeline
except ImportError:
    raise ImportError(
        "You need to install the transformers library to use the MagicPrompt generator. "
        "You can do this by running `pip install -U dynamicprompts[magicprompt]`."
    )

DEFAULT_MODEL_NAME = "Gustavosta/MagicPrompt-Stable-Diffusion"
MAX_SEED = 2 ** 32 - 1



class MagicPromptGenerator(PromptGenerator):
    generator = None
    _model_name = None

    def _load_pipeline(self, model_name: str):
        logger.warning("First load of MagicPrompt may take a while.")

        if MagicPromptGenerator.generator is None:
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForCausalLM.from_pretrained(model_name)

            MagicPromptGenerator.tokenizer = tokenizer
            MagicPromptGenerator.model = model
            MagicPromptGenerator.generator = pipeline(
                task="text-generation", tokenizer=tokenizer, model=model, device=self._device
            )
            MagicPromptGenerator._model_name = model_name

        return MagicPromptGenerator.generator

    def __init__(
        self,
        prompt_generator: PromptGenerator|None=None,
        model_name: str = DEFAULT_MODEL_NAME,
        device: int = -1,
        max_prompt_length: int = 100,
        temperature: float = 0.7,
        seed: int | None = None,
    ):
        self._device = device
        self.set_model(model_name)

        if prompt_generator is None:
            self._prompt_generator = DummyGenerator()
        else:
            self._prompt_generator = prompt_generator

        self._max_prompt_length = max_prompt_length
        self._temperature = float(temperature)
        

        if seed is not None:
            set_seed(int(seed))

    @property
    def model_name(self):
        return self._model_name

    def set_model(self, model_name: str):
        if model_name != MagicPromptGenerator._model_name:
            MagicPromptGenerator._model_name = model_name
            MagicPromptGenerator.generator = None

            self._generator = self._load_pipeline(model_name)
        else:
            self._generator = MagicPromptGenerator.generator
    
    def generate(self, *args, **kwargs) -> List[str]:
        prompts = self._prompt_generator.generate(*args, **kwargs)

        new_prompts = []
        for i in trange(len(prompts), desc="Generating Magic prompts"):
            orig_prompt = prompts[i]
            magic_prompt = self._generator(
                orig_prompt,
                max_length=self._max_prompt_length,
                temperature=self._temperature,
            )[0]["generated_text"]

            magic_prompt = self.clean_up_magic_prompt(orig_prompt, magic_prompt)
            new_prompts.append(magic_prompt)

        return new_prompts

    def clean_up_magic_prompt(self, orig_prompt, prompt):
        # remove the original prompt to keep it out of the MP fixes
        removed_prompt_prefix = False
        if re.search("^" + re.escape(orig_prompt), prompt):
            prompt = prompt.replace(orig_prompt, "", 1)
            removed_prompt_prefix = True

        # old-style weight elevation
        prompt = prompt.translate(str.maketrans("{}", "()")).strip()

        # useless non-word characters at the begin/end
        prompt = re.sub(r"^\W+|\W+$", "", prompt)

        # clean up whitespace in weighted parens
        prompt = re.sub(r"\(\s+", "(", prompt)
        prompt = re.sub(r"\s+\)", ")", prompt)

        # clean up whitespace in hyphens between words
        prompt = re.sub(r"\b\s+\-\s+\b", "-", prompt)
        prompt = re.sub(
            r"\s*[,;\.]+\s*(?=[a-zA-Z(])", ", ", prompt
        )  # other analogues to ', '
        prompt = re.sub(r"\s+_+\s+", " ", prompt)  # useless underscores between phrases
        prompt = re.sub(r"\b,\s*,\s*\b", ", ", prompt)  # empty phrases

        # Translate bangs into proper weight modifiers
        for match in re.findall(r"\b([\w\s\-]+)(\!+)", prompt):
            phrase = match[0]
            full_match = match[0] + match[1]
            weight = round(pow(1.1, len(match[1])), 2)

            prompt = prompt.replace(full_match, f"({phrase}:{weight})")

        # Put the original prompt back in
        if removed_prompt_prefix:
            prompt = orig_prompt + " " + prompt

        return prompt
