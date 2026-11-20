"""多轮对话消息管理模块。

提供 MessageHistory 类，用于管理对话消息历史、
助手消息的 token 统计，以及基于 token 限制的上下文截断。
"""

from typing import List, Dict, Optional, Any


class MessageHistory:
    """管理多轮对话消息和 token 统计。

    内部维护消息列表和助手消息的 usage 信息，
    提供只读的历史消息接口和累计 token 统计。
    """

    def __init__(self, messages=None) -> None:
        self.__messages: List[Dict[str, Any]] = messages if isinstance(messages,list) else []
        self.__usages: List[Dict[str, int]] = []

    def add_system(self, content: str) -> None:
        """添加系统消息。

        Args:
            content: 系统提示词内容。
        """
        self.__messages.append({"role": "system", "content": content})

    def add_user(self, content: str) -> None:
        """添加用户消息。

        Args:
            content: 用户消息内容。
        """
        self.__messages.append({"role": "user", "content": content})

    def add_assistant(self, content: str, usage: Optional[Dict[str, int]] = None) -> None:
        """添加助手消息，并可选记录 usage。

        Args:
            content: 助手回复内容。
            usage: 模型返回的 token 统计信息，如 prompt_tokens、completion_tokens。
        """
        self.__messages.append({"role": "assistant", "content": content})
        if usage:
            self.__usages.append(usage)

    def del_last(self):
        '''删除最后一条消息'''
        self.__messages.pop()

    def get(self) -> List[Dict[str, str]]:
        """返回历史消息，仅暴露 role 和 content。

        Returns:
            由 role 和 content 组成的消息列表。
        """
        return [{"role": m["role"], "content": m["content"]} for m in self.__messages]

    @property  # property 修饰符，超前。property没有魔法
    def total_prompt_tokens(self) -> int:
        """累计 prompt token 数。

        Returns:
            所有助手消息 usage 中 prompt_tokens 的总和。
        """
        return sum(u.get("prompt_tokens", 0) for u in self.__usages)

    @property
    def total_completion_tokens(self) -> int:
        """累计 completion token 数。

        Returns:
            所有助手消息 usage 中 completion_tokens 的总和。
        """
        return sum(u.get("completion_tokens", 0) for u in self.__usages)

    @property
    def total_tokens(self) -> int:
        """累计总 token 数。

        Returns:
           total_tokens 之和。
        """
        return sum(u.get("total_tokens", 0) for u in self.__usages)

    def clear(self) -> None:
        """清空所有消息和 usage 记录。"""
        self.__messages.clear()
        self.__usages.clear()
