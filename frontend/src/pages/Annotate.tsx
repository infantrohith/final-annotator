import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import { useAnnotationStore } from '../store/annotationStore';
import { useKeyboardShortcuts } from '../hooks/useKeyboardShortcuts';
import { AnnotationCanvas } from '../components/AnnotationCanvas';
import { Button } from '../components/Button';
import { Input } from '../components/Input';
import { Loader } from '../components/Loader';
import toast from 'react-hot-toast';
import {
  ArrowLeft,
  Save,
  Trash2,
  Square,
  Download,
  Wand2,
  Tag,
} from 'lucide-react';
import type { Image, Annotation } from '../types';

export const Annotate: React.FC = () => {
  const { imageId } = useParams<{ imageId: string }>();
  const navigate = useNavigate();
  
  const [image, setImage] = useState<Image | null>(null);
  const [loading, setLoading] = useState(true);
  const [currentLabelInput, setCurrentLabelInput] = useState('object');
  
  const {
    annotations,
    selectedAnnotation,
    currentLabel,
    annotationMode,
    setAnnotations,
    setCurrentLabel,
    setAnnotationMode,
    deleteAnnotation,
  } = useAnnotationStore();

  useEffect(() => {
    if (imageId) {
      loadImageAndAnnotations();
    }
  }, [imageId]);

  const loadImageAndAnnotations = async () => {
    if (!imageId) return;

    try {
      const [imageData, annotationsData] = await Promise.all([
        api.getImage(parseInt(imageId)),
        api.getAnnotations({ image_id: parseInt(imageId) }),
      ]);
      setImage(imageData);
      setAnnotations(annotationsData);
    } catch (error) {
      toast.error('Failed to load image');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteAnnotation = async () => {
    if (!selectedAnnotation) return;

    try {
      await api.deleteAnnotation(selectedAnnotation.id);
      deleteAnnotation(selectedAnnotation.id);
      toast.success('Annotation deleted');
    } catch (error) {
      toast.error('Failed to delete annotation');
    }
  };

  const handleAutoAnnotate = async () => {
    if (!imageId) return;

    try {
      toast.loading('Running auto-annotation...', { id: 'auto-annotate' });
      await api.autoAnnotate(parseInt(imageId));
      
      // Reload annotations after a delay
      setTimeout(async () => {
        const annotationsData = await api.getAnnotations({ image_id: parseInt(imageId) });
        setAnnotations(annotationsData);
        toast.success('Auto-annotation completed', { id: 'auto-annotate' });
      }, 3000);
    } catch (error) {
      toast.error('Auto-annotation failed', { id: 'auto-annotate' });
    }
  };

  const handleExport = async () => {
    if (!image?.project_id) {
      toast.error('Image must be in a project to export');
      return;
    }

    try {
      const blob = await api.exportCOCO(image.project_id);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `annotations_${image.project_id}.json`;
      a.click();
      window.URL.revokeObjectURL(url);
      toast.success('Exported successfully');
    } catch (error) {
      toast.error('Export failed');
    }
  };

  const toggleBboxMode = () => {
    setAnnotationMode(annotationMode === 'bbox' ? null : 'bbox');
  };

  const handleLabelChange = () => {
    if (currentLabelInput.trim()) {
      setCurrentLabel(currentLabelInput);
      toast.success(`Label set to: ${currentLabelInput}`);
    }
  };

  // Keyboard shortcuts
  useKeyboardShortcuts([
    {
      key: 'b',
      callback: toggleBboxMode,
      description: 'Toggle bbox mode',
    },
    {
      key: 'Delete',
      callback: handleDeleteAnnotation,
      description: 'Delete selected annotation',
    },
    {
      key: 's',
      ctrl: true,
      callback: (e) => {
        e?.preventDefault();
        toast.success('Annotations auto-saved');
      },
      description: 'Save (auto-saves)',
    },
    {
      key: 'Escape',
      callback: () => {
        setAnnotationMode(null);
      },
      description: 'Cancel drawing mode',
    },
  ]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader size="lg" />
      </div>
    );
  }

  if (!image) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p>Image not found</p>
      </div>
    );
  }

  return (
    <div className="h-screen flex flex-col bg-gray-900">
      {/* Top Toolbar */}
      <div className="bg-gray-800 border-b border-gray-700 px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Button
            variant="ghost"
            size="sm"
            icon={<ArrowLeft size={20} />}
            onClick={() => navigate('/')}
            className="text-white hover:bg-gray-700"
          >
            Back
          </Button>
          <h1 className="text-white font-semibold truncate max-w-md">
            {image.original_filename}
          </h1>
        </div>
        
        <div className="flex items-center gap-2">
          <Button
            variant="secondary"
            size="sm"
            icon={<Wand2 size={18} />}
            onClick={handleAutoAnnotate}
          >
            Auto Annotate
          </Button>
          <Button
            variant="secondary"
            size="sm"
            icon={<Download size={18} />}
            onClick={handleExport}
          >
            Export
          </Button>
        </div>
      </div>

      <div className="flex-1 flex overflow-hidden">
        {/* Left Sidebar */}
        <div className="w-64 bg-gray-800 border-r border-gray-700 p-4 overflow-y-auto">
          <div className="space-y-4">
            {/* Label Input */}
            <div>
              <label className="block text-white text-sm font-medium mb-2">
                <Tag size={16} className="inline mr-1" />
                Current Label
              </label>
              <div className="flex gap-2">
                <Input
                  value={currentLabelInput}
                  onChange={(e) => setCurrentLabelInput(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handleLabelChange()}
                  className="flex-1 bg-gray-700 text-white border-gray-600"
                  placeholder="Enter label"
                />
                <Button size="sm" onClick={handleLabelChange}>
                  Set
                </Button>
              </div>
              <p className="text-xs text-gray-400 mt-1">
                Active: <span className="text-blue-400">{currentLabel}</span>
              </p>
            </div>

            {/* Tools */}
            <div>
              <h3 className="text-white text-sm font-medium mb-2">Tools</h3>
              <div className="space-y-2">
                <Button
                  variant={annotationMode === 'bbox' ? 'primary' : 'secondary'}
                  size="sm"
                  icon={<Square size={18} />}
                  onClick={toggleBboxMode}
                  className="w-full justify-start"
                >
                  Bounding Box (B)
                </Button>
              </div>
            </div>

            {/* Annotations List */}
            <div>
              <h3 className="text-white text-sm font-medium mb-2">
                Annotations ({annotations.length})
              </h3>
              <div className="space-y-1 max-h-96 overflow-y-auto">
                {annotations.map((ann) => (
                  <div
                    key={ann.id}
                    className={`p-2 rounded text-sm cursor-pointer flex items-center justify-between ${
                      selectedAnnotation?.id === ann.id
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-700 text-gray-200 hover:bg-gray-600'
                    }`}
                  >
                    <span className="truncate">{ann.label}</span>
                    {selectedAnnotation?.id === ann.id && (
                      <button
                        onClick={handleDeleteAnnotation}
                        className="ml-2 p-1 hover:bg-red-600 rounded"
                      >
                        <Trash2 size={14} />
                      </button>
                    )}
                  </div>
                ))}
              </div>
            </div>

            {/* Keyboard Shortcuts */}
            <div className="pt-4 border-t border-gray-700">
              <h3 className="text-white text-sm font-medium mb-2">Shortcuts</h3>
              <div className="text-xs text-gray-400 space-y-1">
                <p><kbd className="bg-gray-700 px-1 rounded">B</kbd> Bbox mode</p>
                <p><kbd className="bg-gray-700 px-1 rounded">Delete</kbd> Delete</p>
                <p><kbd className="bg-gray-700 px-1 rounded">Esc</kbd> Cancel</p>
                <p><kbd className="bg-gray-700 px-1 rounded">Ctrl+S</kbd> Save</p>
              </div>
            </div>
          </div>
        </div>

        {/* Canvas Area */}
        <div className="flex-1">
          <AnnotationCanvas
            imageId={parseInt(imageId!)}
            imageUrl={api.getImageUrl(parseInt(imageId!))}
            imageWidth={image.width || 800}
            imageHeight={image.height || 600}
          />
        </div>
      </div>
    </div>
  );
};
