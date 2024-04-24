import sys
from array import array
import moderngl


class Shader:
    def __init__(self) -> None:
        self.ctx = moderngl.create_context()

        self.quad_buffer = self.ctx.buffer(data=array('f', [
            # position (x, y), uv coords (x, y)
            -1.0, 1.0, 0.0, 0.0,  # topleft
            1.0, 1.0, 1.0, 0.0,   # topright
            -1.0, -1.0, 0.0, 1.0, # bottomleft
            1.0, -1.0, 1.0, 1.0,  # bottomright
        ]))

        self.t = 0

        self.vert_shader = '''
        #version 330 core

        in vec2 vert;
        in vec2 texcoord;
        out vec2 uvs;

        void main() {
            uvs = texcoord;
            gl_Position = vec4(vert, 0.0, 1.0);
        }
        '''

        self.frag_shader = '''
        #version 330 core

        uniform sampler2D tex;
        uniform float time;

        in vec2 uvs;
        out vec4 f_color;

        const float noiseIntensity = 0.2;    // Intensity of noise
        const float distortionIntensity = 0.001; // Intensity of distortion
        const float aspectRatio = 4.0 / 4; // Target aspect ratio
        const float screenScale = 1;

        float rand(vec2 co) {
            return fract(sin(dot(co.xy, vec2(12.9898, 78.233)) + time * 0.1) * 43758.5453);
        }

        void main() {
            // Adjust UV coordinates to resize and center the screen
            vec2 scaledUVs = uvs * screenScale + (1.0 - screenScale) / 2.0;
            
            // Apply aspect ratio distortion
            vec2 distortedUVs = scaledUVs * vec2(aspectRatio, 1.0);
            distortedUVs.x += sin(scaledUVs.y * 10 + time * 0.01) * distortionIntensity;
            
            vec4 texColor = texture(tex, distortedUVs);

            // Add moving and random noise
            vec3 noise = vec3(rand(scaledUVs + vec2(time * 0.1, 0.0)) * noiseIntensity);

            // Distort colors
            vec2 distortUVs = scaledUVs + vec2(sin(time * 0.1) * distortionIntensity, cos(time * 0.1) * distortionIntensity);
            vec4 distortedColor = texture(tex, distortUVs);

            // Mix distorted color with original color based on distortionIntensity
            texColor = mix(texColor, distortedColor, distortionIntensity);

            // Apply noise
            f_color = vec4(texColor.rgb - noise, 1.0);
        }
        '''

        self.program = self.ctx.program(vertex_shader=self.vert_shader, fragment_shader=self.frag_shader)
        self.render_object = self.ctx.vertex_array(self.program, [(self.quad_buffer, '2f 2f', 'vert', 'texcoord')])

    def surf_to_texture(self, surf):
        tex = self.ctx.texture(surf.get_size(), 4)
        tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
        tex.swizzle = 'BGRA'
        tex.write(surf.get_view('1'))
        return tex

def update_shader(shader, screen, t):
    frame_tex = shader.surf_to_texture(screen)
    
    frame_tex.use(0)
    shader.program['tex'] = 0
    shader.program['time'] = t
    shader.render_object.render(mode=moderngl.TRIANGLE_STRIP)
    
    frame_tex.release()