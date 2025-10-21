import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import { api } from '../services/api';
import { Button } from '../components/Button';
import { Modal } from '../components/Modal';
import { Input } from '../components/Input';
import { ImageUpload } from '../components/ImageUpload';
import { Loader } from '../components/Loader';
import toast from 'react-hot-toast';
import { FolderPlus, Image as ImageIcon, LogOut, Plus, Folder } from 'lucide-react';
import type { Project, Image } from '../types';

export const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuthStore();
  const [projects, setProjects] = useState<Project[]>([]);
  const [recentImages, setRecentImages] = useState<Image[]>([]);
  const [loading, setLoading] = useState(true);
  const [showProjectModal, setShowProjectModal] = useState(false);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [projectName, setProjectName] = useState('');
  const [projectDescription, setProjectDescription] = useState('');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [projectsData, imagesData] = await Promise.all([
        api.getProjects(0, 10),
        api.getImages({ limit: 12 }),
      ]);
      setProjects(projectsData);
      setRecentImages(imagesData);
    } catch (error) {
      toast.error('Failed to load data');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateProject = async () => {
    if (!projectName.trim()) {
      toast.error('Project name is required');
      return;
    }

    try {
      await api.createProject({
        name: projectName,
        description: projectDescription,
      });
      toast.success('Project created successfully');
      setShowProjectModal(false);
      setProjectName('');
      setProjectDescription('');
      loadData();
    } catch (error) {
      toast.error('Failed to create project');
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader size="lg" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Final Annotator</h1>
            <p className="text-sm text-gray-600">Welcome, {user?.username}!</p>
          </div>
          <div className="flex items-center gap-3">
            <Button
              variant="secondary"
              icon={<Plus size={20} />}
              onClick={() => setShowUploadModal(true)}
            >
              Upload Images
            </Button>
            <Button
              variant="secondary"
              icon={<FolderPlus size={20} />}
              onClick={() => setShowProjectModal(true)}
            >
              New Project
            </Button>
            <Button
              variant="ghost"
              icon={<LogOut size={20} />}
              onClick={handleLogout}
            >
              Logout
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Projects Section */}
        <section className="mb-12">
          <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
            <Folder size={24} />
            Projects
          </h2>
          {projects.length === 0 ? (
            <div className="bg-white rounded-lg shadow p-8 text-center">
              <p className="text-gray-500 mb-4">No projects yet</p>
              <Button onClick={() => setShowProjectModal(true)}>
                Create Your First Project
              </Button>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {projects.map((project) => (
                <div
                  key={project.id}
                  className="bg-white rounded-lg shadow hover:shadow-md transition-shadow p-6 cursor-pointer"
                  onClick={() => navigate(`/projects/${project.id}`)}
                >
                  <h3 className="text-lg font-semibold mb-2">{project.name}</h3>
                  <p className="text-sm text-gray-600 line-clamp-2">
                    {project.description || 'No description'}
                  </p>
                </div>
              ))}
            </div>
          )}
        </section>

        {/* Recent Images Section */}
        <section>
          <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
            <ImageIcon size={24} />
            Recent Images
          </h2>
          {recentImages.length === 0 ? (
            <div className="bg-white rounded-lg shadow p-8 text-center">
              <p className="text-gray-500 mb-4">No images uploaded yet</p>
              <Button onClick={() => setShowUploadModal(true)}>
                Upload Your First Image
              </Button>
            </div>
          ) : (
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {recentImages.map((image) => (
                <div
                  key={image.id}
                  className="bg-white rounded-lg shadow hover:shadow-md transition-shadow overflow-hidden cursor-pointer"
                  onClick={() => navigate(`/annotate/${image.id}`)}
                >
                  <div className="aspect-square bg-gray-200 flex items-center justify-center">
                    <img
                      src={api.getImageUrl(image.id)}
                      alt={image.original_filename}
                      className="w-full h-full object-cover"
                      loading="lazy"
                    />
                  </div>
                  <div className="p-3">
                    <p className="text-sm font-medium truncate">
                      {image.original_filename}
                    </p>
                    <p className="text-xs text-gray-500">{image.status}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>
      </main>

      {/* Modals */}
      <Modal
        isOpen={showProjectModal}
        onClose={() => setShowProjectModal(false)}
        title="Create New Project"
      >
        <div className="space-y-4">
          <Input
            label="Project Name"
            placeholder="Enter project name"
            value={projectName}
            onChange={(e) => setProjectName(e.target.value)}
          />
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Description
            </label>
            <textarea
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows={4}
              placeholder="Enter project description (optional)"
              value={projectDescription}
              onChange={(e) => setProjectDescription(e.target.value)}
            />
          </div>
          <div className="flex gap-2">
            <Button onClick={handleCreateProject} className="flex-1">
              Create
            </Button>
            <Button
              variant="secondary"
              onClick={() => setShowProjectModal(false)}
              className="flex-1"
            >
              Cancel
            </Button>
          </div>
        </div>
      </Modal>

      <Modal
        isOpen={showUploadModal}
        onClose={() => setShowUploadModal(false)}
        title="Upload Images"
        size="lg"
      >
        <ImageUpload
          onUploadComplete={() => {
            setShowUploadModal(false);
            loadData();
          }}
        />
      </Modal>
    </div>
  );
};
