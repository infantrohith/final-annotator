import React, { useCallback, useState } from 'react';
import { Upload, X } from 'lucide-react';
import { api } from '../services/api';
import { Button } from './Button';
import toast from 'react-hot-toast';
import type { Image } from '../types';

interface ImageUploadProps {
  projectId?: number;
  onUploadComplete?: (images: Image[]) => void;
}

export const ImageUpload: React.FC<ImageUploadProps> = ({
  projectId,
  onUploadComplete,
}) => {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  const handleFileSelect = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    const validFiles = files.filter((file) =>
      file.type.startsWith('image/')
    );

    if (validFiles.length !== files.length) {
      toast.error('Some files were not images and were skipped');
    }

    setSelectedFiles((prev) => [...prev, ...validFiles]);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    const files = Array.from(e.dataTransfer.files);
    const validFiles = files.filter((file) =>
      file.type.startsWith('image/')
    );

    if (validFiles.length !== files.length) {
      toast.error('Some files were not images and were skipped');
    }

    setSelectedFiles((prev) => [...prev, ...validFiles]);
  }, []);

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
  };

  const removeFile = (index: number) => {
    setSelectedFiles((prev) => prev.filter((_, i) => i !== index));
  };

  const handleUpload = async () => {
    if (selectedFiles.length === 0) {
      toast.error('Please select files to upload');
      return;
    }

    setUploading(true);
    setUploadProgress(0);

    try {
      const uploadedImages = await api.uploadImages(selectedFiles, projectId);
      
      toast.success(`Successfully uploaded ${uploadedImages.length} images`);
      setSelectedFiles([]);
      setUploadProgress(100);
      
      if (onUploadComplete) {
        onUploadComplete(uploadedImages);
      }
    } catch (error) {
      toast.error('Failed to upload images');
      console.error(error);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="space-y-4">
      <div
        className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-blue-500 transition-colors cursor-pointer"
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onClick={() => document.getElementById('file-input')?.click()}
      >
        <input
          id="file-input"
          type="file"
          multiple
          accept="image/*"
          className="hidden"
          onChange={handleFileSelect}
        />
        <Upload className="mx-auto mb-4 text-gray-400" size={48} />
        <p className="text-lg font-medium text-gray-700">
          Drag and drop images here
        </p>
        <p className="text-sm text-gray-500 mt-2">
          or click to browse files
        </p>
      </div>

      {selectedFiles.length > 0 && (
        <div className="space-y-2">
          <h3 className="font-medium text-gray-700">
            Selected Files ({selectedFiles.length})
          </h3>
          <div className="max-h-48 overflow-y-auto space-y-2">
            {selectedFiles.map((file, index) => (
              <div
                key={index}
                className="flex items-center justify-between p-2 bg-gray-50 rounded"
              >
                <span className="text-sm text-gray-700 truncate flex-1">
                  {file.name}
                </span>
                <button
                  onClick={() => removeFile(index)}
                  className="ml-2 p-1 hover:bg-gray-200 rounded transition-colors"
                  disabled={uploading}
                >
                  <X size={16} />
                </button>
              </div>
            ))}
          </div>

          {uploading && (
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${uploadProgress}%` }}
              />
            </div>
          )}

          <Button
            onClick={handleUpload}
            loading={uploading}
            className="w-full"
          >
            Upload {selectedFiles.length} {selectedFiles.length === 1 ? 'Image' : 'Images'}
          </Button>
        </div>
      )}
    </div>
  );
};
