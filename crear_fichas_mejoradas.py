import pygame

pygame.init()

def crear_ficha_profesional(color_base, nombre_archivo):
    """Crea una ficha con diseño profesional, nítida y compacta"""
    size = 120  # Alta resolución para máxima nitidez
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    center = size // 2
    radius = 55  # Radio más grande para mejor detalle
    
    # Sombra suave multicapa para efecto 3D realista
    for i in range(8):
        shadow_radius = radius + (8 - i)
        shadow_alpha = 35 - i * 4
        pygame.draw.circle(surface, (0, 0, 0, shadow_alpha), 
                         (center + 5 + i//2, center + 5 + i//2), shadow_radius)
    
    if color_base == 'blanco':
        # FICHA BLANCA - Diseño elegante y luminoso
        
        # Base con gradiente radial suave
        for i in range(radius, 0, -1):
            factor = i / radius
            # Gradiente de blanco brillante a blanco perla
            brightness = int(245 + 10 * factor)
            r = min(255, brightness)
            g = min(255, brightness)
            b = min(255, brightness - 5)  # Toque cálido
            pygame.draw.circle(surface, (r, g, b), (center, center), i)
        
        # Reflejo principal (efecto de luz brillante)
        highlight_center_x = center - 15
        highlight_center_y = center - 15
        for i in range(25, 0, -1):
            alpha = int(200 * ((i / 25) ** 3))
            pygame.draw.circle(surface, (255, 255, 255, alpha), 
                             (highlight_center_x, highlight_center_y), i)
        
        # Reflejo secundario pequeño
        for i in range(8, 0, -1):
            alpha = int(120 * ((i / 8) ** 2))
            pygame.draw.circle(surface, (255, 255, 255, alpha), 
                             (center + 18, center + 18), i)
        
        # Bordes con efecto metálico profesional
        # Borde exterior oscuro
        pygame.draw.circle(surface, (130, 130, 140), (center, center), radius, 5)
        # Borde medio brillante
        pygame.draw.circle(surface, (220, 220, 230), (center, center), radius - 3, 2)
        # Borde interior sutil
        pygame.draw.circle(surface, (180, 180, 190), (center, center), radius - 6, 1)
        
    else:
        # FICHA NEGRA - Diseño elegante y profundo
        
        # Base con gradiente radial profundo
        for i in range(radius, 0, -1):
            factor = i / radius
            # Gradiente de gris oscuro a negro profundo
            brightness = int(50 * (0.2 + 0.8 * factor))
            r = brightness
            g = brightness
            b = min(brightness + 8, 65)  # Toque azulado
            pygame.draw.circle(surface, (r, g, b), (center, center), i)
        
        # Reflejo principal (luz reflejada sutil)
        highlight_center_x = center - 15
        highlight_center_y = center - 15
        for i in range(20, 0, -1):
            alpha = int(140 * ((i / 20) ** 3))
            brightness = int(80 + 40 * (i / 20))
            pygame.draw.circle(surface, (brightness, brightness, brightness + 10, alpha), 
                             (highlight_center_x, highlight_center_y), i)
        
        # Reflejo secundario muy sutil
        for i in range(6, 0, -1):
            alpha = int(80 * ((i / 6) ** 2))
            pygame.draw.circle(surface, (90, 90, 100, alpha), 
                             (center + 20, center + 20), i)
        
        # Bordes elegantes oscuros
        # Borde exterior muy oscuro
        pygame.draw.circle(surface, (15, 15, 15), (center, center), radius, 5)
        # Borde medio con brillo metálico
        pygame.draw.circle(surface, (80, 80, 90), (center, center), radius - 3, 2)
        # Borde interior sutil
        pygame.draw.circle(surface, (50, 50, 60), (center, center), radius - 6, 1)
    
    # Guardar imagen
    pygame.image.save(surface, f'assets/{nombre_archivo}')
    print(f'✓ Creada: {nombre_archivo} ({size}x{size} px) - Alta calidad')

# Crear ambas fichas
print("\n🎨 Generando fichas profesionales de alta calidad...")
print("=" * 50)
crear_ficha_profesional('blanco', 'checker_white.png')
crear_ficha_profesional('negro', 'checker_black.png')
print("=" * 50)
print("✨ ¡Fichas profesionales creadas exitosamente!")
print("   - Resolución: 120x120 px")
print("   - Efectos 3D mejorados")
print("   - Bordes metálicos")
print("   - Reflejos realistas\n")
