import axios, { AxiosInstance } from 'axios';
import type {
  AuthResponse,
  LoginCredentials,
  RegisterData,
  Project,
  Image,
  Annotation,
  CreateAnnotation,
  VisionTask,
  MLModel,
} from '../types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: `${API_URL}/api/v1`,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add auth token to requests
    this.api.interceptors.request.use((config) => {
      const token = localStorage.getItem('token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    // Handle 401 errors
    this.api.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('token');
          localStorage.removeItem('user');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // Auth endpoints
  async register(data: RegisterData): Promise<AuthResponse> {
    const response = await this.api.post<AuthResponse>('/auth/register', data);
    return response.data;
  }

  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const response = await this.api.post<AuthResponse>('/auth/login', credentials);
    return response.data;
  }

  // Project endpoints
  async getProjects(skip = 0, limit = 100): Promise<Project[]> {
    const response = await this.api.get<Project[]>('/projects/', {
      params: { skip, limit },
    });
    return response.data;
  }

  async createProject(data: { name: string; description?: string }): Promise<Project> {
    const response = await this.api.post<Project>('/projects/', data);
    return response.data;
  }

  async getProject(id: number): Promise<Project> {
    const response = await this.api.get<Project>(`/projects/${id}`);
    return response.data;
  }

  async updateProject(id: number, data: Partial<Project>): Promise<Project> {
    const response = await this.api.put<Project>(`/projects/${id}`, data);
    return response.data;
  }

  async deleteProject(id: number): Promise<void> {
    await this.api.delete(`/projects/${id}`);
  }

  // Image endpoints
  async getImages(params?: {
    skip?: number;
    limit?: number;
    project_id?: number;
    status_filter?: string;
  }): Promise<Image[]> {
    const response = await this.api.get<Image[]>('/images/', { params });
    return response.data;
  }

  async uploadImage(file: File, projectId?: number): Promise<Image> {
    const formData = new FormData();
    formData.append('file', file);
    if (projectId) {
      formData.append('project_id', projectId.toString());
    }

    const response = await this.api.post<Image>('/images/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  }

  async uploadImages(files: File[], projectId?: number): Promise<Image[]> {
    const formData = new FormData();
    files.forEach((file) => formData.append('files', file));
    if (projectId) {
      formData.append('project_id', projectId.toString());
    }

    const response = await this.api.post<Image[]>('/images/upload-batch', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  }

  async getImage(id: number): Promise<Image> {
    const response = await this.api.get<Image>(`/images/${id}`);
    return response.data;
  }

  getImageUrl(id: number): string {
    const token = localStorage.getItem('token');
    return `${API_URL}/api/v1/images/${id}/file?token=${token}`;
  }

  async updateImage(id: number, data: Partial<Image>): Promise<Image> {
    const response = await this.api.put<Image>(`/images/${id}`, data);
    return response.data;
  }

  async deleteImage(id: number): Promise<void> {
    await this.api.delete(`/images/${id}`);
  }

  // Annotation endpoints
  async getAnnotations(params?: {
    skip?: number;
    limit?: number;
    image_id?: number;
    label?: string;
  }): Promise<Annotation[]> {
    const response = await this.api.get<Annotation[]>('/annotations/', { params });
    return response.data;
  }

  async createAnnotation(data: CreateAnnotation): Promise<Annotation> {
    const response = await this.api.post<Annotation>('/annotations/', data);
    return response.data;
  }

  async createAnnotations(data: CreateAnnotation[]): Promise<Annotation[]> {
    const response = await this.api.post<Annotation[]>('/annotations/batch', data);
    return response.data;
  }

  async updateAnnotation(id: number, data: Partial<Annotation>): Promise<Annotation> {
    const response = await this.api.put<Annotation>(`/annotations/${id}`, data);
    return response.data;
  }

  async deleteAnnotation(id: number): Promise<void> {
    await this.api.delete(`/annotations/${id}`);
  }

  // Vision task endpoints
  async getTasks(params?: {
    skip?: number;
    limit?: number;
    task_type?: string;
    status_filter?: string;
  }): Promise<VisionTask[]> {
    const response = await this.api.get<VisionTask[]>('/tasks/', { params });
    return response.data;
  }

  async detectObjects(imageId: number): Promise<VisionTask> {
    const response = await this.api.post<VisionTask>(`/tasks/detect/${imageId}`);
    return response.data;
  }

  async classifyImage(imageId: number): Promise<VisionTask> {
    const response = await this.api.post<VisionTask>(`/tasks/classify/${imageId}`);
    return response.data;
  }

  async autoAnnotate(imageId: number): Promise<{ message: string; image_id: number }> {
    const response = await this.api.post(`/tasks/auto-annotate/${imageId}`);
    return response.data;
  }

  async getTask(id: number): Promise<VisionTask> {
    const response = await this.api.get<VisionTask>(`/tasks/${id}`);
    return response.data;
  }

  // ML Model endpoints
  async getModels(params?: {
    skip?: number;
    limit?: number;
    status_filter?: string;
  }): Promise<MLModel[]> {
    const response = await this.api.get<MLModel[]>('/models/', { params });
    return response.data;
  }

  async createModel(data: { name: string; model_type: string }): Promise<MLModel> {
    const response = await this.api.post<MLModel>('/models/', data);
    return response.data;
  }

  async trainModel(
    id: number,
    params?: { epochs?: number; batch_size?: number; learning_rate?: number }
  ): Promise<MLModel> {
    const response = await this.api.post<MLModel>(`/models/${id}/train`, null, { params });
    return response.data;
  }

  async predict(modelId: number, imageId: number): Promise<any> {
    const response = await this.api.post(`/models/${modelId}/predict`, null, {
      params: { image_id: imageId },
    });
    return response.data;
  }

  // Export endpoints
  async exportCOCO(projectId: number): Promise<Blob> {
    const response = await this.api.get(`/export/coco/${projectId}`, {
      responseType: 'blob',
    });
    return response.data;
  }

  async exportYOLO(projectId: number): Promise<Blob> {
    const response = await this.api.get(`/export/yolo/${projectId}`, {
      responseType: 'blob',
    });
    return response.data;
  }

  async exportPascalVOC(projectId: number): Promise<Blob> {
    const response = await this.api.get(`/export/pascal-voc/${projectId}`, {
      responseType: 'blob',
    });
    return response.data;
  }
}

export const api = new ApiService();
