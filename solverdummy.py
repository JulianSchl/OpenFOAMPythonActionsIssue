import numpy as np
import precice

configuration_file_name = 'precice-config.xml'
participant_name = 'Solid'
write_data_name = 'Displacement_Data'
read_data_name = 'Force_Data'
mesh_name = 'Solid-Mesh'

num_vertices = 10  # Number of vertices

solver_process_index = 0
solver_process_size = 1

interface = precice.Interface(participant_name, configuration_file_name,
                              solver_process_index, solver_process_size)

mesh_id = interface.get_mesh_id(mesh_name)

#assert (interface.is_mesh_connectivity_required(mesh_id) is False)

dimensions = interface.get_dimensions()

vertices = np.zeros((num_vertices, dimensions))
read_data = np.zeros((num_vertices, dimensions))
write_data = np.zeros((num_vertices, dimensions))

x = 0.5
vertices = np.array((np.ones((num_vertices))*x,np.linspace(-0.09,0.02,num_vertices))).T
read_data = vertices
write_data = vertices
write_data *= 0

vertex_ids = interface.set_mesh_vertices(mesh_id, vertices)
read_data_id = interface.get_data_id(read_data_name, mesh_id)
write_data_id = interface.get_data_id(write_data_name, mesh_id)
dt = interface.initialize()

while interface.is_coupling_ongoing():
    if interface.is_action_required(
            precice.action_write_iteration_checkpoint()):
        print("DUMMY: Writing iteration checkpoint")
        interface.mark_action_fulfilled(
            precice.action_write_iteration_checkpoint())

    if interface.is_read_data_available():
        read_data = interface.read_block_vector_data(read_data_id, vertex_ids)

    write_data = write_data #+ 10**(-9)

    if interface.is_write_data_required(dt):
        interface.write_block_vector_data(
            write_data_id, vertex_ids, write_data)

    print("DUMMY: Advancing in time")
    dt = interface.advance(dt)

    if interface.is_action_required(
            precice.action_read_iteration_checkpoint()):
        print("DUMMY: Reading iteration checkpoint")
        interface.mark_action_fulfilled(
            precice.action_read_iteration_checkpoint())

interface.finalize()
print("DUMMY: Closing python solver dummy...")
