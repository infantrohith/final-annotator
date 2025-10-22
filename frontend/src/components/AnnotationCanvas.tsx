import React, { useRef, useEffect, useState, useCallback } from 'react';
import { useAnnotationStore } from '../store/annotationStore';
import type { Annotation, CreateAnnotation } from '../types';
import toast from 'react-hot-toast';
import { api } from '../services/api';

interface AnnotationCanvasProps {
  imageId: number;
  imageUrl: string;
  imageWidth: number;
  imageHeight: number;
  onAnnotationCreate?: (annotation: Annotation) => void;
}

export const AnnotationCanvas: React.FC<AnnotationCanvasProps> = ({
  imageId,
  imageUrl,
  imageWidth,
  imageHeight,
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const imageRef = useRef<HTMLImageElement>(null);
  
  const [scale, setScale] = useState(1);
  const [offset, setOffset] = useState({ x: 0, y: 0 });
  const [isPanning, setIsPanning] = useState(false);
  const [panStart, setPanStart] = useState({ x: 0, y: 0 });
  
  const {
    annotations,
    selectedAnnotation,
    currentLabel,
    annotationMode,
    isDrawing,
    tempAnnotation,
    setIsDrawing,
    setTempAnnotation,
    addAnnotation,
    selectAnnotation,
  } = useAnnotationStore();

  const [drawStart, setDrawStart] = useState<{ x: number; y: number } | null>(null);

  // Load and draw image
  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas?.getContext('2d');
    if (!canvas || !ctx) return;

    const img = new Image();
    img.crossOrigin = 'anonymous';
    img.src = imageUrl;
    
    img.onload = () => {
      imageRef.current = img;
      
      // Calculate scale to fit container
      const container = containerRef.current;
      if (container) {
        const containerWidth = container.clientWidth;
        const containerHeight = container.clientHeight;
        const scaleX = containerWidth / img.width;
        const scaleY = containerHeight / img.height;
        const newScale = Math.min(scaleX, scaleY, 1);
        setScale(newScale);
        
        canvas.width = img.width;
        canvas.height = img.height;
        
        drawCanvas();
      }
    };
  }, [imageUrl]);

  // Redraw canvas when annotations or temp annotation changes
  useEffect(() => {
    drawCanvas();
  }, [annotations, tempAnnotation, selectedAnnotation, scale, offset]);

  const drawCanvas = useCallback(() => {
    const canvas = canvasRef.current;
    const ctx = canvas?.getContext('2d');
    const img = imageRef.current;
    
    if (!canvas || !ctx || !img) return;

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw image
    ctx.drawImage(img, 0, 0);

    // Draw all annotations
    annotations.forEach((ann) => {
      const isSelected = selectedAnnotation?.id === ann.id;
      drawAnnotation(ctx, ann, isSelected);
    });

    // Draw temporary annotation
    if (tempAnnotation && tempAnnotation.x !== undefined) {
      ctx.strokeStyle = '#00ff00';
      ctx.lineWidth = 2;
      ctx.setLineDash([5, 5]);
      ctx.strokeRect(
        tempAnnotation.x,
        tempAnnotation.y || 0,
        tempAnnotation.width || 0,
        tempAnnotation.height || 0
      );
      ctx.setLineDash([]);
    }
  }, [annotations, tempAnnotation, selectedAnnotation]);

  const drawAnnotation = (
    ctx: CanvasRenderingContext2D,
    ann: Annotation,
    isSelected: boolean
  ) => {
    if (ann.annotation_type === 'bbox' && ann.x !== undefined) {
      ctx.strokeStyle = isSelected ? '#ff0000' : '#00ffff';
      ctx.fillStyle = isSelected ? 'rgba(255, 0, 0, 0.1)' : 'rgba(0, 255, 255, 0.1)';
      ctx.lineWidth = isSelected ? 3 : 2;

      ctx.fillRect(ann.x, ann.y!, ann.width!, ann.height!);
      ctx.strokeRect(ann.x, ann.y!, ann.width!, ann.height!);

      // Draw label
      ctx.fillStyle = isSelected ? '#ff0000' : '#00ffff';
      ctx.font = '14px Arial';
      const textMetrics = ctx.measureText(ann.label);
      ctx.fillRect(ann.x, ann.y! - 20, textMetrics.width + 10, 20);
      ctx.fillStyle = '#000000';
      ctx.fillText(ann.label, ann.x + 5, ann.y! - 5);
    }
  };

  const getCanvasCoordinates = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) return { x: 0, y: 0 };

    const rect = canvas.getBoundingClientRect();
    const x = (e.clientX - rect.left) / scale;
    const y = (e.clientY - rect.top) / scale;

    return { x, y };
  };

  const handleMouseDown = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const coords = getCanvasCoordinates(e);

    // Check if clicking on existing annotation
    const clickedAnn = annotations.find((ann) => {
      if (ann.annotation_type === 'bbox' && ann.x !== undefined) {
        return (
          coords.x >= ann.x &&
          coords.x <= ann.x + ann.width! &&
          coords.y >= ann.y! &&
          coords.y <= ann.y! + ann.height!
        );
      }
      return false;
    });

    if (clickedAnn) {
      selectAnnotation(clickedAnn);
      return;
    }

    // Start drawing new annotation
    if (annotationMode === 'bbox') {
      setIsDrawing(true);
      setDrawStart(coords);
      setTempAnnotation({
        image_id: imageId,
        label: currentLabel,
        annotation_type: 'bbox',
        x: coords.x,
        y: coords.y,
        width: 0,
        height: 0,
      });
    }
  };

  const handleMouseMove = (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (!isDrawing || !drawStart || !tempAnnotation) return;

    const coords = getCanvasCoordinates(e);
    const width = coords.x - drawStart.x;
    const height = coords.y - drawStart.y;

    setTempAnnotation({
      ...tempAnnotation,
      width,
      height,
    });
  };

  const handleMouseUp = async (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (!isDrawing || !tempAnnotation) return;

    setIsDrawing(false);

    // Only create annotation if it has some size
    if (Math.abs(tempAnnotation.width || 0) > 5 && Math.abs(tempAnnotation.height || 0) > 5) {
      try {
        // Normalize coordinates (handle negative width/height)
        const normalizedAnn: CreateAnnotation = {
          image_id: imageId,
          label: currentLabel,
          annotation_type: 'bbox',
          x: tempAnnotation.width! < 0 ? tempAnnotation.x! + tempAnnotation.width! : tempAnnotation.x!,
          y: tempAnnotation.height! < 0 ? tempAnnotation.y! + tempAnnotation.height! : tempAnnotation.y!,
          width: Math.abs(tempAnnotation.width!),
          height: Math.abs(tempAnnotation.height!),
        };

        const created = await api.createAnnotation(normalizedAnn);
        addAnnotation(created);
        toast.success('Annotation created');
      } catch (error) {
        toast.error('Failed to create annotation');
        console.error(error);
      }
    }

    setTempAnnotation(null);
    setDrawStart(null);
  };

  const handleWheel = (e: React.WheelEvent<HTMLCanvasElement>) => {
    e.preventDefault();
    const delta = e.deltaY > 0 ? 0.9 : 1.1;
    setScale((prev) => Math.min(Math.max(prev * delta, 0.1), 5));
  };

  return (
    <div
      ref={containerRef}
      className="relative w-full h-full overflow-hidden bg-gray-900"
      style={{ cursor: annotationMode ? 'crosshair' : 'default' }}
    >
      <canvas
        ref={canvasRef}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onWheel={handleWheel}
        style={{
          transform: `scale(${scale}) translate(${offset.x}px, ${offset.y}px)`,
          transformOrigin: 'top left',
        }}
        className="absolute top-0 left-0"
      />
    </div>
  );
};
