// Type definitions
export interface User {
  id: number;
  username: string;
  email: string;
  is_active: boolean;
  is_superuser: boolean;
  created_at: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface Project {
  id: number;
  name: string;
  description?: string;
  owner_id: number;
  created_at: string;
  updated_at: string;
}

export interface Image {
  id: number;
  filename: string;
  filepath: string;
  original_filename: string;
  width?: number;
  height?: number;
  file_size?: number;
  mime_type?: string;
  project_id?: number;
  uploader_id: number;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface Annotation {
  id: number;
  image_id: number;
  label: string;
  annotation_type: string;
  x?: number;
  y?: number;
  width?: number;
  height?: number;
  coordinates?: Array<{ x: number; y: number }>;
  confidence?: number;
  metadata?: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface CreateAnnotation {
  image_id: number;
  label: string;
  annotation_type: string;
  x?: number;
  y?: number;
  width?: number;
  height?: number;
  coordinates?: Array<{ x: number; y: number }>;
  confidence?: number;
  metadata?: Record<string, any>;
}

export interface VisionTask {
  id: number;
  name: string;
  task_type: string;
  status: string;
  progress: number;
  config?: Record<string, any>;
  results?: Record<string, any>;
  error_message?: string;
  created_at: string;
  updated_at: string;
  completed_at?: string;
}

export interface MLModel {
  id: number;
  name: string;
  model_type: string;
  status: string;
  accuracy?: number;
  loss?: number;
  epochs_trained: number;
  config?: Record<string, any>;
  model_path?: string;
  training_info?: Record<string, any>;
  created_at: string;
  updated_at: string;
  completed_at?: string;
}
