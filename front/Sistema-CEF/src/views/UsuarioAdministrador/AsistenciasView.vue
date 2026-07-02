

<template>
  <v-container>
    <h1>Asistencias</h1>
    <p>Esta es la vista de asistencias para administradores.</p>
    <v-row>
      <v-col cols="12">
        <v-data-table :headers="headers" :items="asistencias" class="elevation-1">
          <template v-slot:item="{ item }">
            <tr>
              <td>{{ item.nombre }}</td>
              <td>{{ item.fecha }}</td>
              <td>{{ item.estado }}</td>
            </tr>
          </template>
        </v-data-table>
      </v-col>
    </v-row>
  </v-container>
</template>


