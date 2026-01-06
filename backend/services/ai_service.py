"""DeepSeek API integration service"""
import requests
import os
from typing import Dict, List, Optional


class AIService:
    """Service for interacting with DeepSeek API"""
    
    def __init__(self, api_key: str, api_base: str = "https://api.deepseek.com/v1"):
        """
        Initialize AI service
        
        Args:
            api_key: DeepSeek API key
            api_base: DeepSeek API base URL
        """
        self.api_key = api_key
        self.api_base = api_base
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def summarize_chapter(
        self,
        chapter_text: str,
        chapter_title: str,
        temperature: float = 0.7,
        max_tokens: int = 4000
    ) -> str:
        """
        Generate detailed chapter summary using DeepSeek V3
        
        Args:
            chapter_text: The chapter content
            chapter_title: The chapter title
            temperature: Model temperature (0-1)
            max_tokens: Maximum tokens in response
            
        Returns:
            Detailed chapter summary in Markdown format
        """
        prompt = f"""请对以下教科书章节进行详细总结：

章节标题：{chapter_title}

章节内容：
{chapter_text}

请提供以下内容：
1. 主要内容概述（100-200字）
2. 关键概念列表（列出5-10个重要术语及其定义）
3. 重点知识点（详细说明需要掌握的核心内容）
4. 难点解析（简化复杂概念的解释）
5. 学习建议（如何更好地理解和记忆）

请使用清晰的Markdown格式输出。"""

        data = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system",
                    "content": "你是一个专业的教育助手，擅长分析和总结教科书内容，帮助学生更好地理解学习材料。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        try:
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers=self.headers,
                json=data,
                timeout=120
            )
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                raise Exception(
                    f"API调用失败: {response.status_code} - {response.text}"
                )
        except requests.exceptions.Timeout:
            raise Exception("API请求超时，请稍后重试")
        except Exception as e:
            raise Exception(f"API调用出错: {str(e)}")
    
    def answer_question(
        self,
        question: str,
        context: str,
        chapter_title: str = "",
        conversation_history: Optional[List[Dict]] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """
        Answer questions based on chapter content
        
        Args:
            question: User's question
            context: Chapter content or relevant context
            chapter_title: Optional chapter title
            conversation_history: Optional conversation history
            temperature: Model temperature
            max_tokens: Maximum tokens in response
            
        Returns:
            Answer to the question
        """
        messages = [
            {
                "role": "system",
                "content": "你是一个专业的教育助手，擅长回答关于教科书内容的问题。请基于提供的章节内容给出详细、准确的回答。"
            }
        ]
        
        # Add conversation history if available
        if conversation_history:
            messages.extend(conversation_history)
        
        # Build user prompt
        user_prompt = f"章节内容：\n{context}\n\n"
        if chapter_title:
            user_prompt = f"章节标题：{chapter_title}\n\n" + user_prompt
        user_prompt += f"问题：{question}\n\n请基于以上章节内容回答问题。"
        
        messages.append({
            "role": "user",
            "content": user_prompt
        })
        
        data = {
            "model": "deepseek-chat",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        try:
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers=self.headers,
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                raise Exception(
                    f"API调用失败: {response.status_code} - {response.text}"
                )
        except requests.exceptions.Timeout:
            raise Exception("API请求超时，请稍后重试")
        except Exception as e:
            raise Exception(f"API调用出错: {str(e)}")
