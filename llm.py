import os
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple, List, Dict, Any, Optional

import numpy as np
import torch
import yaml
from torch import device as torch_device

from utils.tools import get_md5
from synthesize import synthesize, generate_synthesis_args, preprocess_english, preprocess_mandarin, SPLIT_LIMIT
from text.emotion import process_emotion
from utils.model import get_model, get_vocoder


@dataclass
class PathConfig:
    base_dir: Path
    checkpoint_dir: Path
    result_dir: Path

    @classmethod
    def create_default(cls, base_dir: str = "./output") -> 'PathConfig':
        base = Path(base_dir)
        return cls(
            base_dir=base,
            checkpoint_dir=base / "ckpt" / "ESD",
            result_dir=base / "result" / "ESD"
        )

    def ensure_dirs(self):
        """确保所有必要的目录存在"""
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.result_dir.mkdir(parents=True, exist_ok=True)

    def get_result_path(self, filename: str) -> Path:
        """获取结果文件的完整路径"""
        return self.result_dir / filename


@dataclass
class SynthesisConfig:
    preprocess_config: Dict[str, Any]
    model_config: Dict[str, Any]
    train_config: Dict[str, Any]

    @classmethod
    def from_yaml_files(cls, preprocess_path: str, model_path: str, train_path: str) -> 'SynthesisConfig':
        """从YAML文件加载配置"""

        def load_yaml(path: str) -> Dict[str, Any]:
            with open(path, 'r') as f:
                return yaml.safe_load(f)

        return cls(
            preprocess_config=load_yaml(preprocess_path),
            model_config=load_yaml(model_path),
            train_config=load_yaml(train_path)
        )

    @property
    def configs(self) -> Tuple[Dict[str, Any], ...]:
        """返回配置元组"""
        return (self.preprocess_config, self.model_config, self.train_config)


class SpeechSynthesizer:
    def __init__(self, output_dir: Optional[str] = None):
        self.device = torch_device("cuda" if torch.cuda.is_available() else "cpu")
        self.paths = PathConfig.create_default(output_dir or "./output")
        self.paths.ensure_dirs()

        self.args = self._generate_args()
        self.config = self._load_config()
        self.model = self._init_model()
        self.vocoder = self._init_vocoder()

        print(f"Results will be saved to: {self.paths.result_dir}")

    def _generate_args(self):
        """生成参数"""
        args_dict = {
            "restore_step": 18000,
            "mode": "single",
            "preprocess_config": "./config/ESD/preprocess.yaml",
            "model_config": "./config/ESD/model.yaml",
            "train_config": "./config/ESD/train.yaml",
        }
        # 修复参数生成方式
        args_list = []
        for key, value in args_dict.items():
            args_list.extend([f"--{key}", str(value)])
        return generate_synthesis_args(args_list)

    def _load_config(self) -> SynthesisConfig:
        """加载配置文件"""
        return SynthesisConfig.from_yaml_files(
            self.args.preprocess_config,
            self.args.model_config,
            self.args.train_config
        )

    def _init_model(self):
        """初始化模型"""
        return get_model(self.args, self.config.configs, self.device, train=False)

    def _init_vocoder(self):
        """初始化声码器"""
        return get_vocoder(self.config.model_config, self.device)

    def _preprocess_text(self, text: str) -> np.ndarray:
        """根据语言预处理文本"""
        language = self.config.preprocess_config["preprocessing"]["text"]["language"]
        if language == "en":
            return preprocess_english(text, self.config.preprocess_config)
        elif language == "zh":
            return preprocess_mandarin(text, self.config.preprocess_config)
        else:
            raise ValueError(f"Unsupported language: {language}")

    def get_output_path(self, filename: str) -> Path:
        """获取输出文件的完整路径"""
        return self.paths.get_result_path(filename)

    def generate(
            self,
            text: str,
            speaker_id: int = 0,
            emotion: str = "Neutral",
            max_text_length: int = SPLIT_LIMIT,
    ) -> Path:
        """
        生成语音

        Args:
            text: 要合成的文本
            speaker_id: 说话人ID
            emotion: 情感类型
            max_text_length: 最大文本长度

        Returns:
            Path: 生成的音频文件路径
        """
        # 预处理输入
        truncated_text = text[:max_text_length]
        ids = raw_texts = [truncated_text]
        speakers = np.array([speaker_id])
        processed_emotion = np.array([process_emotion(emotion)])

        # 文本处理
        processed_text = np.array([self._preprocess_text(truncated_text)])
        text_lens = np.array([len(processed_text[0])])
        batch = [(
            ids,
            raw_texts,
            speakers,
            processed_emotion,
            processed_text,
            text_lens,
            max(text_lens)
        )]

        # 控制参数
        control_values = (
            self.args.pitch_control,
            self.args.energy_control,
            self.args.duration_control
        )

        # 合成
        synthesize(
            self.model,
            self.args.restore_step,
            self.config.configs,
            self.vocoder,
            batch,
            control_values
        )

        return self.get_output_path(f"{get_md5(text[:SPLIT_LIMIT])}.wav")


def main():
    # 可以指定自定义输出目录
    synthesizer = SpeechSynthesizer()
    output_path = synthesizer.generate(
        "test me again",
    )
    print(f"Audio generated at: {output_path}")


if __name__ == "__main__":
    main()