# Interview Guide

## 1. What is your project?
It is an AI-powered interview practice application that generates personalized questions and evaluates candidate answers with an LLM API.

## 2. What problem does it solve?
It gives candidates focused practice and immediate feedback instead of generic question lists.

## 3. What is the domain?
AI tooling and education, applicable across technical and non-technical interview contexts.

## 4. Why Python?
Python is productive for API integration, validation, testing, and data-oriented application logic.

## 5. Why Streamlit?
Streamlit provides a responsive Python UI quickly without adding a separate JavaScript frontend stack.

## 6. What is an LLM?
A Large Language Model learns patterns from large text datasets and generates language conditioned on a prompt.

## 7. Why use an LLM?
It can generate varied, context-aware questions and nuanced feedback across roles and domains.

## 8. What is an LLM API?
It is a network interface that lets an application send prompts to a hosted language model and receive generated output.

## 9. How does the application communicate with the LLM?
The dedicated client sends system and user messages requesting JSON, then parses and validates the response.

## 10. What is prompt engineering?
It is the design of instructions and context that guide a model toward useful, consistent output.

## 11. How are questions personalized?
The prompt includes role, experience, skills, domain, difficulty, type, and requested count.

## 12. How is difficulty controlled?
The prompt explains the reasoning level expected for easy, medium, hard, or mixed questions; validation also checks the returned structure.

## 13. How are answers evaluated?
The model receives the question, expected answer, criteria, rubric, and candidate answer, then returns a 0-10 score and feedback.

## 14. What is hallucination?
It is plausible-sounding but inaccurate or fabricated model output.

## 15. How do you reduce hallucinations?
Use constrained inputs, explicit prompts, structured output, response validation, and human review.

## 16. Why not train your own LLM?
Training requires substantial data, compute, expertise, and maintenance; an API is more practical for this lightweight project.

## 17. Why did you not use RAG?
RAG was outside the original core requirement. The first version directly uses user input, prompts, and the LLM API.

## 18. How would you add RAG?
Add document ingestion, chunking, embeddings, retrieval, and relevant context in the generation prompt, with careful source validation.

## 19. What are the limitations?
The app depends on provider availability, model quality, and network access; local history is single-user and model feedback is not authoritative.

## 20. What happens if the API fails?
The client converts expected provider errors into friendly messages, and the current session remains intact so the user can retry.