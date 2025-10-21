import { create } from 'zustand';
import type { Annotation, CreateAnnotation } from '../types';

interface AnnotationState {
  annotations: Annotation[];
  selectedAnnotation: Annotation | null;
  currentLabel: string;
  annotationMode: 'bbox' | 'polygon' | 'point' | null;
  isDrawing: boolean;
  tempAnnotation: Partial<CreateAnnotation> | null;
  setAnnotations: (annotations: Annotation[]) => void;
  addAnnotation: (annotation: Annotation) => void;
  updateAnnotation: (id: number, data: Partial<Annotation>) => void;
  deleteAnnotation: (id: number) => void;
  selectAnnotation: (annotation: Annotation | null) => void;
  setCurrentLabel: (label: string) => void;
  setAnnotationMode: (mode: 'bbox' | 'polygon' | 'point' | null) => void;
  setIsDrawing: (drawing: boolean) => void;
  setTempAnnotation: (annotation: Partial<CreateAnnotation> | null) => void;
  clearAnnotations: () => void;
}

export const useAnnotationStore = create<AnnotationState>((set) => ({
  annotations: [],
  selectedAnnotation: null,
  currentLabel: 'object',
  annotationMode: null,
  isDrawing: false,
  tempAnnotation: null,

  setAnnotations: (annotations) => set({ annotations }),

  addAnnotation: (annotation) =>
    set((state) => ({
      annotations: [...state.annotations, annotation],
    })),

  updateAnnotation: (id, data) =>
    set((state) => ({
      annotations: state.annotations.map((ann) =>
        ann.id === id ? { ...ann, ...data } : ann
      ),
    })),

  deleteAnnotation: (id) =>
    set((state) => ({
      annotations: state.annotations.filter((ann) => ann.id !== id),
      selectedAnnotation:
        state.selectedAnnotation?.id === id ? null : state.selectedAnnotation,
    })),

  selectAnnotation: (annotation) =>
    set({ selectedAnnotation: annotation }),

  setCurrentLabel: (label) => set({ currentLabel: label }),

  setAnnotationMode: (mode) => set({ annotationMode: mode }),

  setIsDrawing: (drawing) => set({ isDrawing: drawing }),

  setTempAnnotation: (annotation) => set({ tempAnnotation: annotation }),

  clearAnnotations: () =>
    set({
      annotations: [],
      selectedAnnotation: null,
      tempAnnotation: null,
    }),
}));
