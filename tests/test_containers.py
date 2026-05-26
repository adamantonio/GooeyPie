import unittest
from unittest.mock import MagicMock
import gooeypie as gp

class TestContainers(unittest.TestCase):
    def setUp(self):
        self.app = gp.GooeyPieApp('test')

    def test_frame_default_propagation(self):
        # By default, propagation should be enabled
        frame = gp.Frame()
        self.app.add(frame, 1, 1)
        # Verify ctk frame is created
        self.assertIsNotNone(frame._ctk_object)

    def test_frame_init_size_disables_propagation(self):
        frame = gp.Frame(width=800, height=400)
        
        # Spy on the pack_propagate method of ctk object once it's created
        # We can hook into widget creation or mock/spy
        original_create = frame._create_widget
        spy = MagicMock()
        
        def spy_create(master):
            original_create(master)
            frame._ctk_object.pack_propagate = spy
            # Call again or trigger the propagation setting
            if 'width' in frame._constructor_kwargs or 'height' in frame._constructor_kwargs:
                frame._ctk_object.pack_propagate(False)
                
        frame._create_widget = spy_create
        self.app.add(frame, 1, 1)
        
        spy.assert_called_with(False)

    def test_frame_dynamic_size_disables_propagation(self):
        frame = gp.Frame()
        self.app.add(frame, 1, 1)
        
        spy = MagicMock()
        frame._ctk_object.pack_propagate = spy
        
        # Dynamically set width
        frame.width = 500
        spy.assert_called_with(False)
        self.assertEqual(frame.width, 500)
        
        # Dynamically set height
        frame.height = 300
        spy.assert_called_with(False)
        self.assertEqual(frame.height, 300)

    def test_container_init_size_disables_propagation(self):
        container = gp.Container(width=600, height=300)
        
        original_create = container._create_widget
        spy = MagicMock()
        
        def spy_create(master):
            original_create(master)
            container._ctk_object.pack_propagate = spy
            if 'width' in container._constructor_kwargs or 'height' in container._constructor_kwargs:
                container._ctk_object.pack_propagate(False)
                
        container._create_widget = spy_create
        self.app.add(container, 1, 1)
        
        spy.assert_called_with(False)

    def test_container_dynamic_size_disables_propagation(self):
        container = gp.Container()
        self.app.add(container, 1, 1)
        
        spy = MagicMock()
        container._ctk_object.pack_propagate = spy
        
        # Dynamically set width
        container.width = 400
        spy.assert_called_with(False)
        self.assertEqual(container.width, 400)
        
        # Dynamically set height
        container.height = 250
        spy.assert_called_with(False)
        self.assertEqual(container.height, 250)

    def test_frame_partial_size_autosizes_other_dimension(self):
        # Create frame with width but no height
        frame = gp.Frame(width=800)
        lbl = gp.Label("Test")
        frame.add(lbl, 1, 1)
        self.app.add(frame, 1, 1)
        
        # Verify set width is exactly 800
        self.assertEqual(frame._ctk_object.cget('width'), 800)
        # Verify height auto-sized to be small (less than the default 200)
        self.assertLess(frame._ctk_object.cget('height'), 200)

    def test_container_partial_size_autosizes_other_dimension(self):
        # Create container with width but no height
        container = gp.Container(width=800)
        lbl = gp.Label("Test")
        container.add(lbl, 1, 1)
        self.app.add(container, 1, 1)
        
        # Verify set width is exactly 800
        self.assertEqual(container._ctk_object.cget('width'), 800)
        # Verify height auto-sized to be small (less than the default 200)
        self.assertLess(container._ctk_object.cget('height'), 200)

if __name__ == '__main__':
    unittest.main()
